package com.example.redis_mysql_web.mapper;

import com.example.redis_mysql_web.pojo.Course;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.io.IOException;
import java.util.List;

@Mapper
public interface CourseMapper {
    // 该方法使用了带一个参数的查询语句，返回一条记录
    public Course findCourseByNumber(String course_number) throws IOException;

    // 更新 course 信息
    public int updateCourseByNumber(Course course);

    // 直接使用 @Select()注解
    @Select("SELECT * FROM course_information")
    public List<Course> getAllCourse();

    // 该方法插入一条记录，带参数，更新操作一定要提交事务
    public int addCourse(Course course);
}
