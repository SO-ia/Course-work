package com.example.redis_mysql_web.service;

import com.example.redis_mysql_web.pojo.Stu;

import java.io.IOException;
import java.util.List;

public interface StuService {
    public Stu findStuByNumber(String number) throws IOException;

    public String updateStuByNumber(Stu stu);

    public List<Stu> getAllStu();

    public int addStu(Stu stu);
}
