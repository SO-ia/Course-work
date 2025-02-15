package com.example.redis_mysql_web.service;

import com.example.redis_mysql_web.pojo.Course;

import java.io.IOException;
import java.util.List;

public interface CourseService {
    public Course findCourseByNumber(String course_number) throws IOException;

    public Course updateCourseByNumber(Course course);

    public List<Course> getAllCourse();

    public int addCourse(Course course);
}
