package com.example.redis_mysql_web.service.impl;

import com.example.redis_mysql_web.mapper.GradeMapper;
import com.example.redis_mysql_web.pojo.Grade;
import com.example.redis_mysql_web.service.GradeService;
import com.example.redis_mysql_web.util.GradeBloomFilterUtil;
import jakarta.annotation.Resource;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

/**
 *  缓存击穿问题，需用的方法
 *方法 1: queryWithLock()--处理缓存击穿问题
 *方法 2: addlock()--申请锁
 *方法 3：unlock()--释放锁
 *
 */

/**
 * 缓存穿透使用 Redission 内的布隆过滤器解决
 */
@Service
public class GradeServiceImpl implements GradeService {
    @Resource
    private GradeMapper gradeMapper;
    @Resource
    private RedisTemplate redisTemplate;
    @Resource
    GradeBloomFilterUtil gradeBloomFilterUtil;

    // 缓存击穿
    // 1.通过互斥锁--处理缓存击穿问题
    public Grade queryWithLock(String grade_number) throws IOException {
        String key = "grade:" + grade_number;
        Grade grade = getGradeByRedis(grade_number);

        // 1.首先到 gradeBloomFilterUtil 中查找该grade是否存在
        if(!gradeBloomFilterUtil.checkBloomFilter(grade_number)) {
            System.out.println("布隆过滤器中没有该成绩信息!!");
//            return null;
        }

        System.out.println(grade);
        // 2.如果 Redis 中有该grade，则直接返回
        if (grade != null) {
            System.out.println("Redis缓存中查询到此grade");
            return grade;
        }

        System.out.println("Redis缓存中没有此grade");

        //3.准备互斥锁的 key
        String lockKey = "lock:grade:" + grade_number;

        // 4.Redis中没有，表示查询未命中，则需进行加锁和缓存重建（查询 mysql）
        try {
            //4.1获取锁,调用 addLock()方法
            boolean isLock = addLock(lockKey);
            //4.2 判断锁是否获取成功. 这里判断加锁失败，则休眠，然后再次执行该方法
            if (!isLock) {
                Thread.sleep(50);
                //休眠 50毫秒后，再次执行该方法，递归调用，重新查询 redis
                return queryWithLock(grade_number);
            }

            System.out.println("Redis申请锁成功！");

            //4.3 如果成功加上了锁，要再次查询 redis 缓存是否有该数据，
            // 因为可能有其他应用--已重建了该数据的缓存
            if (getGradeByRedis(grade_number) != null) {
                System.out.println("再次查询时，Redis缓存中查询到此grade");
                return grade;
            }

            // 5. 这里表示，两次查询 Redis，都没有查询到数据，
            // 则要到 mysql中查询,重建缓存
            // 5.1如果 mysql中也没有，则将空对象写入 redis
            grade = gradeMapper.findGradeByNumber(grade_number);

            //5.2模拟缓存重建延迟了
            Thread.sleep(200);

            //5.3数据库里也没有，redis中也没有,向redis 中写入空对象null
            if (grade == null) {
                System.out.println("Mysql中也没有此grade");
                Grade s = new Grade();
                s.setGrade_number(grade_number);
                saveToRedis(s);
            } else {
                //5.4 mysql中有该grade，将该数据写入redis,重建数据成功
                System.out.println("Mysql中查询到此grade");
                saveToRedis(grade);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            // 6.删除互斥锁
            unLock(lockKey);
        }
        return grade;
    }

    //2.加锁--在 redis端使用setnx key value命令加锁
    private boolean addLock(String key) {
        Boolean flag = redisTemplate.opsForValue().setIfAbsent(key, "1", 10,
                TimeUnit.SECONDS);
        //   return BooleanUtil.isTrue(flag) ;
        return flag;
    }

    //3.释放锁
    private void unLock(String key) {
        redisTemplate.delete(key);
    }

    //4. 应用：查询热点数据，使用queryWithLock方法
    public Grade findGradeByNumber(String grade_number) throws IOException {
        // 调用queryWithLock方法
        Grade grade = queryWithLock(grade_number);
        return grade;
    }


    //从redis中查询Grade
    public Grade getGradeByRedis(String grade_number) {
        String key = "grade:" + grade_number;
        if (redisTemplate.hasKey(key)) {
            String course_number = (String) redisTemplate.opsForHash().get(key, "course_number");
            String student_number = (String) redisTemplate.opsForHash().get(key, "student_number");
            Double grade = (Double) redisTemplate.opsForHash().get(key, "grade");

            Grade tmpGrade = new Grade();
            tmpGrade.setGrade_number(grade_number);
            tmpGrade.setCourse_number(course_number);
            tmpGrade.setStudent_number(student_number);
            tmpGrade.setGrade(grade);
            return tmpGrade;
        }
        return null;
    }

    //保存 grade 信息到Redis,使用hash类型
    public void saveToRedis(Grade grade) {
        //设置key: grade:ID
        String key = "grade:" + grade.getGrade_number();
        //各字段的值都存入Redis
        redisTemplate.opsForHash().put(key, "grade", grade.getGrade());
        redisTemplate.opsForHash().put(key, "grade_number", grade.getGrade_number());
        redisTemplate.opsForHash().put(key, "course_number", grade.getCourse_number());
        redisTemplate.opsForHash().put(key, "course_name", grade.getCourse_name());
        redisTemplate.opsForHash().put(key, "student_number", grade.getStudent_number());
        redisTemplate.opsForHash().put(key, "student_name", grade.getStudent_name());

        // 设置key的过期时间为6分钟
        // redisTemplate.expire(key, 360, TimeUnit.SECONDS);
        // 创建一个随机的 KEY 的有效期
        int expiredTime= 360 + new Random().nextInt(100);
        redisTemplate.expire(key,expiredTime, TimeUnit.SECONDS);
    }


    // 根据 id 修改grade信息
    // 考虑更新操作，确保redis缓存一致性
    @Transactional   // 开启事务
    public Grade updateGradeByNumber(Grade grade) {
        String grade_number = grade.getGrade_number();
        if (grade_number == null) {
            System.out.println("grade_number不能为空");
        }
        //修改1. 先更新mysql数据库
        gradeMapper.updateGradeByNumber(grade);
        //修改2. 后Redis删除缓存
        String key = "grade:" + grade_number;
        redisTemplate.delete(key);
        String newInfo = grade.toString();
//        return "更新成功";
        System.out.println("更新成功");
        System.out.println(newInfo);
        return grade;
    }

    //查询grade
    public List<Grade> getAllGrade() {
        return gradeMapper.getAllGrade();
    }

    public int addGrade(Grade grade) {
        return gradeMapper.addGrade(grade);
    }

    //处理：缓存穿透问题
    public Grade queryWithPassThrough(String grade_number) throws IOException {
        //1.查看Redis缓存中是否有数据
        Grade grade = getGradeByRedis(grade_number);

        //2.如果Redis中有该grade，则返回
        if (grade != null) {
            System.out.println("Redis缓存中查询到此grade");
            return grade;
        }

        // 3.Redis中没有，则到mysql中查询,
        // 如果mysql中也没有，则将空对象写入redis
        System.out.println("Redis缓存中没有此grade");
        grade = gradeMapper.findGradeByNumber(grade_number);
        if (grade == null) {
            System.out.println("Mysql中也没有此grade");
            Grade newGrade = new Grade();
            newGrade.setGrade_number(grade_number);
            saveToRedis(newGrade);
        } else {
            System.out.println("Mysql中查询到此grade");
            saveToRedis(grade);
        }
        return grade;
    }

}
