package com.example.redis_mysql_web.service;

import com.example.redis_mysql_web.pojo.Grade;

import java.io.IOException;
import java.util.List;

public interface GradeService {
    public Grade findGradeByNumber(String grade_number) throws IOException;

    public Grade updateGradeByNumber(Grade grade);

    public List<Grade> getAllGrade();

    public int addGrade(Grade grade);
}
