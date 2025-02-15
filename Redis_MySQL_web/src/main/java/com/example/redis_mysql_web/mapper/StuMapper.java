package com.example.redis_mysql_web.mapper;

import com.example.redis_mysql_web.pojo.Stu;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.io.IOException;
import java.util.List;

@Mapper
public interface StuMapper {
    // 该方法使用了带一个参数的查询语句，返回一条记录
    public Stu findStuByNumber(String number) throws IOException;

    // 更新用户信息
    public int updateStuByNumber(Stu stu);

    //   直接使用 @Select()注解
    @Select("SELECT * FROM students")
    public List<Stu> getAllStu();

    // 该方法插入一条记录，带参数，更新操作一定要提交事务
    public int addStu(Stu stus);
}
