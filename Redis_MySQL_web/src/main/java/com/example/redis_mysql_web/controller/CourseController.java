package com.example.redis_mysql_web.controller;

import com.example.redis_mysql_web.pojo.Course;
import com.example.redis_mysql_web.service.CourseService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
public class CourseController {
    @Resource
    public CourseService courseService;

    // 1.访问number=S001的合法用户
    // URL:  http://localhost:8080/findCourseByNumber/S004
    @RequestMapping("/findCourseByNumber/{course_number}")
    public Course findCourseByNumber(@PathVariable String course_number) throws IOException {
        Course course= courseService.findCourseByNumber(course_number);
        System.out.println(course);
        return course;
    }

    // 2.访问S009的不合法用户
    // URL:  http://localhost:8080/findCourseByFilter
    @RequestMapping("/findCourseByFilter")
    public Course findCourseByBloomFilter() throws IOException {
        String course_number="CSE000";
        Course course= courseService.findCourseByNumber(course_number);
        System.out.println(course);
        return course;
    }

    // 3.1 修改 course 信息
    // URL:  http://localhost:8080/updateByNumber/
    @RequestMapping("/updateCourseByNumber/{course_number}")
    public Course updateCourseByNumber(@PathVariable String course_number) throws IOException {
//        course.setCourse_number("S004");
        Course course = courseService.findCourseByNumber(course_number);
        course.setCourse_name(course.getCourse_name()+"改");
        course.setCourse_opening_semester(course.getCourse_opening_semester() + "改");
        Course newCourse= courseService.updateCourseByNumber(course);
        System.out.println(newCourse);
        return newCourse;
    }

    // 3.2 html修改 course 信息
    // URL:  http://localhost:8080/updateHtmlByNumber
    @RequestMapping("/updateCourseHtmlByNumber/{course_number}")
    public Course updateCourseHtmlByNumber(@PathVariable String course_number, @RequestBody Course updatedCourse) throws IOException {
        Course existingCourse = courseService.findCourseByNumber(course_number);
        if (existingCourse != null) {
            existingCourse.setCourse_name(updatedCourse.getCourse_name());
            existingCourse.setCourse_opening_semester(updatedCourse.getCourse_opening_semester());
            existingCourse.setCourse_department(updatedCourse.getCourse_department());
            courseService.updateCourseByNumber(existingCourse);  // Assuming updateCourseByNumber method exists
//            return "course信息更新成功：\n" + existingCourse;
            System.out.println("更新成功");
            return existingCourse;
        } else {
            System.out.println("course信息未找到，更新失败。");
            return null;
        }
    }

    // 4.直接插入course信息
    // URL:  http://localhost:8080/insertCourseInfo
    @RequestMapping("/insertCourseInfo")
    public String insertCourseInfo(){
        Course newCourse=new Course();
        newCourse.setCourse_number("CSE102");
        newCourse.setCourse_name("插入新课程名");
        newCourse.setCourse_opening_semester("插入新课程学期");
        newCourse.setCourse_department("插入新课程开设系");
        // 验证传入的course数据
        if (newCourse == null || newCourse.getCourse_number() == null || newCourse.getCourse_name() == null || newCourse.getCourse_opening_semester() == null) {
            return "无效的course数据";
        }
        // 将course插入数据库
        int result = courseService.addCourse(newCourse);

        if (result > 0) {
            System.out.println(newCourse);
            return newCourse.toString();
        } else {
            return "course信息插入失败。";
        }
    }

    // 5.html插入course信息
    // URL:  http://localhost:8080/insertHtmlInfo
    @RequestMapping("/insertCourseHtmlInfo")
    public Course insertCourseHtmlInfo(@RequestBody Course newCourse){
        // 验证传入的course数据
//        System.out.println(newCourse.toString());
        if (newCourse == null || newCourse.getCourse_number() == null || newCourse.getCourse_name() == null || newCourse.getCourse_opening_semester() == null) {
            System.out.println("course数据无效");
            return null;
        }
        // 将course插入数据库
        int result = courseService.addCourse(newCourse);

        if (result > 0) {
            System.out.println("course插入成功");
            return newCourse;
        } else {
//            return "信息插入失败。";
            System.out.println("course插入失败");
            return null;
        }
    }
}
