package com.example.redis_mysql_web.mapper;

import com.example.redis_mysql_web.pojo.Grade;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.io.IOException;
import java.util.List;

@Mapper
public interface GradeMapper {
    // 该方法使用了带一个参数的查询语句，返回一条记录
    public Grade findGradeByNumber(String grade_number) throws IOException;

    // 更新 grade 信息
    public int updateGradeByNumber(Grade grade);

    // 直接使用 @Select()注解
    @Select("SELECT * FROM student_grades")
    public List<Grade> getAllGrade();

    // 该方法插入一条记录，带参数，更新操作一定要提交事务
    public int addGrade(Grade grade);
}
