package com.example.redis_mysql_web.service.impl;

import com.example.redis_mysql_web.mapper.CourseMapper;
import com.example.redis_mysql_web.pojo.Course;
import com.example.redis_mysql_web.service.CourseService;
import com.example.redis_mysql_web.util.CourseBloomFilterUtil;
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
public class CourseServiceImpl implements CourseService {
    @Resource
    private CourseMapper courseMapper;
    @Resource
    private RedisTemplate redisTemplate;
    @Resource
    CourseBloomFilterUtil courseBloomFilterUtil;

    // 缓存击穿
    // 1.通过互斥锁--处理缓存击穿问题
    public Course queryWithLock(String course_number) throws IOException {
        String key = "course:" + course_number;
        Course course = getCourseByRedis(course_number);

        // 1.首先到 courseBloomFilterUtil 中查找该course是否存在
        if(!courseBloomFilterUtil.checkBloomFilter(course_number)) {
            System.out.println("布隆过滤器中没有该课程信息!!");
            return null;
        }

        // 2.如果 Redis 中有该course，则直接返回
        if (course != null) {
            System.out.println("Redis缓存中查询到此course");
            return course;
        }

        System.out.println("Redis缓存中没有此course");

        //3.准备互斥锁的 key
        String lockKey = "lock:course:" + course_number;

        // 4.Redis中没有，表示查询未命中，则需进行加锁和缓存重建（查询 mysql）
        try {
            //4.1获取锁,调用 addLock()方法
            boolean isLock = addLock(lockKey);
            //4.2 判断锁是否获取成功. 这里判断加锁失败，则休眠，然后再次执行该方法
            if (!isLock) {
                Thread.sleep(50);
                //休眠 50毫秒后，再次执行该方法，递归调用，重新查询 redis
                return queryWithLock(course_number);
            }

            System.out.println("Redis申请锁成功！");

            //4.3 如果成功加上了锁，要再次查询 redis 缓存是否有该数据，
            // 因为可能有其他应用--已重建了该数据的缓存
            if (getCourseByRedis(course_number) != null) {
                System.out.println("再次查询时，Redis缓存中查询到此course");
                return course;
            }

            // 5. 这里表示，两次查询 Redis，都没有查询到数据，
            // 则要到 mysql中查询,重建缓存
            // 5.1如果 mysql中也没有，则将空对象写入 redis
            course = courseMapper.findCourseByNumber(course_number);

            //5.2模拟缓存重建延迟了
            Thread.sleep(200);

            //5.3数据库里也没有，redis中也没有,向redis 中写入空对象null
            if (course == null) {
                System.out.println("Mysql中也没有此course");
                Course s = new Course();
                s.setCourse_number(course_number);
                saveToRedis(s);
            } else {
                //5.4 mysql中有该course，将该数据写入redis,重建数据成功
                System.out.println("Mysql中查询到此course");
                saveToRedis(course);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            // 6.删除互斥锁
            unLock(lockKey);
        }
        return course;
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
    public Course findCourseByNumber(String course_number) throws IOException {
        // 调用queryWithLock方法
        Course course = queryWithLock(course_number);
        return course;
    }

    //处理：缓存穿透问题
    public Course queryWithPassThrough(String course_number) throws IOException {
        //1.查看Redis缓存中是否有数据
        Course course = getCourseByRedis(course_number);

        //2.如果Redis中有该course，则返回
        if (course != null) {
            System.out.println("Redis缓存中查询到此course");
            return course;
        }

        // 3.Redis中没有，则到mysql中查询,
        // 如果mysql中也没有，则将空对象写入redis
        System.out.println("Redis缓存中没有此course");
        course = courseMapper.findCourseByNumber(course_number);
        if (course == null) {
            System.out.println("Mysql中也没有此course");
            Course newCourse = new Course();
            newCourse.setCourse_number(course_number);
            saveToRedis(newCourse);
        } else {
            System.out.println("Mysql中查询到此course");
            saveToRedis(course);
        }
        return course;
    }

    //从redis中查询Course
    public Course getCourseByRedis(String course_number) {
        String key = "course:" + course_number;
        if (redisTemplate.hasKey(key)) {
            String course_name = (String) redisTemplate.opsForHash().get(key, "course_name");
            String course_opening_semester = (String) redisTemplate.opsForHash().get(key, "course_opening_semester");
            String course_department = (String) redisTemplate.opsForHash().get(key, "course_department");
//            String stu_number= (String) redisTemplate.opsForHash().get(key,"stu_number");
            Course course = new Course();
            course.setCourse_number(course_number);
            course.setCourse_name(course_name);
            course.setCourse_opening_semester(course_opening_semester);
            course.setCourse_department(course_department);
            //  System.out.print(course);
            return course;
        }
        return null;
    }

    //保存 course 信息到Redis,使用hash类型
    public void saveToRedis(Course course) {
        //设置key: course:ID
        String key = "course:" + course.getCourse_number();
        //各字段的值都存入Redis
        redisTemplate.opsForHash().put(key, "course_name", course.getCourse_name());
        redisTemplate.opsForHash().put(key, "course_number", course.getCourse_number());
        redisTemplate.opsForHash().put(key, "course_opening_semester", course.getCourse_opening_semester());
        redisTemplate.opsForHash().put(key, "course_department", course.getCourse_department());

        // 设置key的过期时间为6分钟
        // redisTemplate.expire(key, 360, TimeUnit.SECONDS);
        // 创建一个随机的 KEY 的有效期
        int expiredTime= 360 + new Random().nextInt(100);
        redisTemplate.expire(key,expiredTime, TimeUnit.SECONDS);
    }


    // 根据 id 修改course信息
    // 考虑更新操作，确保redis缓存一致性
    @Transactional   // 开启事务
    public Course updateCourseByNumber(Course course) {
        String course_number = course.getCourse_number();
        if (course_number == null) {
            System.out.println("course_number不能为空");
        }
        //修改1. 先更新mysql数据库
        courseMapper.updateCourseByNumber(course);
        //修改2. 后Redis删除缓存
        String key = "course:" + course_number;
        redisTemplate.delete(key);
        String newInfo = course.toString();
//        return "更新成功";
        System.out.println("更新成功");
        System.out.println(newInfo);
        return course;
    }

    //查询course
    public List<Course> getAllCourse() {
        return courseMapper.getAllCourse();
    }

    public int addCourse(Course course) {
        return courseMapper.addCourse(course);
    }
}
