package com.example.redis_mysql_web.service.impl;

import com.example.redis_mysql_web.mapper.StuMapper;
import com.example.redis_mysql_web.pojo.Stu;
import com.example.redis_mysql_web.service.StuService;
import com.example.redis_mysql_web.util.StuBloomFilterUtil;
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
public class StuServiceImpl implements StuService {
    @Resource
    private StuMapper stuMapper;
    @Resource
    private RedisTemplate redisTemplate;
    @Resource
    StuBloomFilterUtil stuBloomFilterUtil;

    // 缓存击穿
    // 1.通过互斥锁--处理缓存击穿问题
        // 1.1首先到stuBloomFilter中查找该stu是否存在
    // 2.如果 Redis 中有该stu，则直接返回
    // 3.准备互斥锁的 key
    // 4.Redis中没有，表示查询未命中，则需进行加锁和缓存重建（查询 mysql）
        // 4.1获取锁,调用 addLock()方法
        // 4.2 判断锁是否获取成功. 这里判断加锁失败，则休眠，然后再次执行该方法
        // 休眠 50毫秒后，再次执行该方法，递归调用，重新查询 redis
    // 4.3 如果成功加上了锁，要再次查询 redis 缓存是否有该数据，
        // 因为可能有其他应用--已重建了该数据的缓存
    // 5. 这里表示，两次查询 Redis，都没有查询到数据，
        // 则要到 mysql中查询,重建缓存
        // 5.1如果 mysql中也没有，则将空对象写入 redis
        // 5.2模拟缓存重建延迟了
        // 5.3数据库里也没有，redis中也没有,向redis 中写入空对象null
        // 5.4 mysql中有该student，将该数据写入redis,重建数据成功
    // 6.删除互斥锁

    public Stu queryWithLock(String number) throws IOException {
        String key = "stu:" + number;
        Stu stu = getStuByRedis(number);

        //1.首先到stuBloomFilter中查找该stu是否存在
        if(!stuBloomFilterUtil.checkBloomFilter(number)) {
            System.out.println("布隆过滤器中未查询到此学生");
            return null;
        }

        //2.如果 Redis 中有该stu，则直接返回
        if (stu != null) {
            System.out.println("Redis缓存中查询到此学生信息");
            return stu;
        }

        System.out.println("Redis缓存中没有此学生信息");

        // 3.准备互斥锁的 key
        String lockKey = "lock:stu:" + number;

        // 4.Redis中没有，表示查询未命中，则需进行加锁和缓存重建（查询 mysql）
        try {
            //4.1获取锁,调用 addLock()方法
            boolean isLock = addLock(lockKey);
            //4.2 判断锁是否获取成功. 这里判断加锁失败，则休眠，然后再次执行该方法
            if (!isLock) {
                Thread.sleep(50);
                //休眠 50毫秒后，再次执行该方法，递归调用，重新查询 redis
                return queryWithLock(number);
            }

            System.out.println("Redis申请锁成功！");

            //4.3 如果成功加上了锁，要再次查询 redis 缓存是否有该数据，
            // 因为可能有其他应用--已重建了该数据的缓存
            if (getStuByRedis(number) != null) {
                System.out.println("再次查询时，Redis缓存中查询到此学生信息");
                return stu;
            }

            // 5. 这里表示，两次查询 Redis，都没有查询到数据，
            // 则要到 mysql中查询,重建缓存
            // 5.1如果 mysql中也没有，则将空对象写入 redis
            stu = stuMapper.findStuByNumber(number);

            //5.2模拟缓存重建延迟了
            Thread.sleep(200);

            //5.3数据库里也没有，redis中也没有,向redis 中写入空对象null
            if (stu == null) {
                System.out.println("Mysql中也没有此学生信息");
                Stu s = new Stu();
                s.setStudent_number(number);
                saveToRedis(s);
            } else {
                //5.4 mysql中有该student，将该数据写入redis,重建数据成功
                System.out.println("Mysql中查询到此学生信息");
                saveToRedis(stu);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            // 6.删除互斥锁
            unLock(lockKey);
        }
        return stu;
    }

    // 2.加锁--在 redis端使用setnx key value命令加锁
    private boolean addLock(String key) {
        Boolean flag = redisTemplate.opsForValue().setIfAbsent(key, "1", 10,
                TimeUnit.SECONDS);
        //   return BooleanUtil.isTrue(flag) ;
        return flag;
    }

    // 3.释放锁
    private void unLock(String key) {
        redisTemplate.delete(key);
    }

    // 4. 应用：查询热点数据，使用queryWithLock方法
    public Stu findStuByNumber(String number) throws IOException {
        // 调用queryWithLock方法
        Stu stu = queryWithLock(number);
        return stu;
    }


    // 处理：缓存穿透问题
    // 已在上方函数中处理
    public Stu queryWithPassThrough(String number) throws IOException {
        //1.查看Redis缓存中是否有数据
        Stu stu = getStuByRedis(number);

        //2.如果Redis中有该student，则返回
        if (stu != null) {
            System.out.println("Redis缓存中查询到此学生信息");
            return stu;
        }

        // 3.Redis中没有，则到mysql中查询,
        // 如果mysql中也没有，则将空对象写入redis
        System.out.println("Redis缓存中没有此学生信息");
        stu = stuMapper.findStuByNumber(number);
        if (stu == null) {
            System.out.println("Mysql中也没有此学生信息");
            Stu newStu = new Stu();
            newStu.setStudent_number(number);
            saveToRedis(newStu);
        } else {
            System.out.println("Mysql中查询到此学生信息");
            saveToRedis(stu);
        }
        return stu;
    }

    //从redis中查询User
    public Stu getStuByRedis(String number) {
        String key = "stu:" + number;
        if (redisTemplate.hasKey(key)) {
            String name = (String) redisTemplate.opsForHash().get(key, "name");
            String gender = (String) redisTemplate.opsForHash().get(key, "gender");
//            String stu_number= (String) redisTemplate.opsForHash().get(key,"stu_number");
            Stu stu = new Stu();
            stu.setStudent_number(number);
            stu.setName(name);
            stu.setGender(gender);
            //  System.out.print(stu);
            return stu;
        }
        return null;
    }

    //保存Stu信息到Redis,使用hash类型
    public void saveToRedis(Stu stu) {
        //设置key: stu:ID
        String key = "stu:" + stu.getStudent_number();
        //各字段的值都存入Redis
        redisTemplate.opsForHash().put(key, "name", stu.getName());
        redisTemplate.opsForHash().put(key, "student_number", stu.getStudent_number());
        redisTemplate.opsForHash().put(key, "gender", stu.getGender());

        // 设置key的过期时间为6分钟
        // redisTemplate.expire(key, 360, TimeUnit.SECONDS);
        // 创建一个随机的 KEY 的有效期
        int expiredTime= 360 + new Random().nextInt(100);
        redisTemplate.expire(key,expiredTime, TimeUnit.SECONDS);
    }


    // 根据number修改student信息
    // 考虑更新操作，确保redis缓存一致性
    @Transactional   // 开启事务
    public String updateStuByNumber(Stu stu) {
        String number = stu.getStudent_number();
        if (number == null) {
            return "student学号不能为空";
        }
        //修改1. 先更新mysql数据库
        stuMapper.updateStuByNumber(stu);
        //修改2. 后Redis删除缓存
        String key = "stu:" + number;
        redisTemplate.delete(key);
        String newInfo = stu.toString();
//        return "更新成功";
        System.out.println("更新成功");
        System.out.println(newInfo);
        return newInfo;
    }

    //查询student
    public List<Stu> getAllStu() {
        return stuMapper.getAllStu();
    }

    public int addStu(Stu stu) {
        return stuMapper.addStu(stu);
    }
}
