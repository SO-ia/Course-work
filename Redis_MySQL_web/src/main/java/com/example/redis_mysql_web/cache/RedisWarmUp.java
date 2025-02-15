package com.example.redis_mysql_web.cache;

import com.example.redis_mysql_web.mapper.CourseMapper;
import com.example.redis_mysql_web.mapper.GradeMapper;
import com.example.redis_mysql_web.mapper.StuMapper;
import com.example.redis_mysql_web.pojo.Course;
import com.example.redis_mysql_web.pojo.Grade;
import com.example.redis_mysql_web.pojo.Stu;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Random;
import java.util.concurrent.TimeUnit;

/*
 * Redis缓存预热:实现ApplicationRunner接口
 * 项目启动时，自动将所有表中的数据 加载到 redis 缓存
 *
 */
@Component
public class RedisWarmUp implements ApplicationRunner {
    @Resource
    private StuMapper stuMapper;
    @Resource
    private RedisTemplate redisTemplate;
    @Autowired
    private CourseMapper courseMapper;
    @Autowired
    private GradeMapper gradeMapper;

    // 预热缓存
    @Override
    public void run(ApplicationArguments args) throws Exception {
        // 从数据库获取所有学生信息
        List<Stu> stuList = stuMapper.getAllStu();
        List<Course> courseList = courseMapper.getAllCourse();
        List<Grade> gradeList = gradeMapper.getAllGrade();
        // 将所有学生信息加载到 Redis 缓存中
        for (Stu stu : stuList) {
            saveStuToRedis(stu);
        }
        for (Course course : courseList) {
            saveCourseToRedis(course);
        }
        for (Grade grade : gradeList) {
            saveGradeToRedis(grade);
        }

        System.out.println("缓存预热完成: 所有数据已加载到 Redis");
    }

    // 将单个学生数据保存到 Redis
    private void saveStuToRedis(Stu stu) {
        // 设置 Redis 缓存的 Key
        String key = "stu:" + stu.getStudent_number();

        // 使用 Redis 的 Hash 类型存储学生信息
        redisTemplate.opsForHash().put(key, "name", stu.getName());
        redisTemplate.opsForHash().put(key, "student_number", stu.getStudent_number());
        redisTemplate.opsForHash().put(key, "gender", stu.getGender());

        // 设置缓存的过期时间，避免缓存无限期存在
        int expiredTime = 360 + (int)(Math.random() * 100);  // 设置一个随机过期时间
        redisTemplate.expire(key, expiredTime, TimeUnit.SECONDS);
    }

    //保存 grade 信息到Redis,使用hash类型
    public void saveGradeToRedis(Grade grade) {
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

    //保存 course 信息到Redis,使用hash类型
    public void saveCourseToRedis(Course course) {
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


//    @Override
//    public void run(ApplicationArguments args) throws Exception {
//        System.out.println("初始化库存数据： 200....");
//        String key="stock";
//        redisTemplate.opsForValue().set(key, 200);
//
//    }
}
