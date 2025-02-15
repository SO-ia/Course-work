package com.example.redis_mysql_web.controller;

import com.example.redis_mysql_web.pojo.Grade;
import com.example.redis_mysql_web.service.GradeService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
public class GradeController {
    @Resource
    public GradeService gradeService;

    // 1.访问合法成绩
    // URL:  http://localhost:8080/findGradeByNumber/S10002/A101
    @RequestMapping("/findGradeByNumber/{student_number}/{course_number}")
    public Grade findGradeByNumber(@PathVariable String student_number, @PathVariable String course_number) throws IOException {
        String grade_number = student_number + ":" + course_number;
        System.out.println(grade_number);
        Grade grade= gradeService.findGradeByNumber(grade_number);
        System.out.println(grade);
        return grade;
    }

    // 2.访问不合法成绩
    // URL:  http://localhost:8080/findGradeByFilter
    @RequestMapping("/findGradeByFilter")
    public Grade findGradeByBloomFilter() throws IOException {
        String grade_number="S10001/C000000000";
        Grade grade= gradeService.findGradeByNumber(grade_number);
        System.out.println(grade);
        return grade;
    }

    // 3.1 修改 grade 信息
    // URL:  http://localhost:8080/updateByNumber/S10003:C102
    @RequestMapping("/updateByNumber/{grade_number:.*}")
    public Grade updateGradeByNumber(@PathVariable String grade_number) throws IOException {
        Grade grade = gradeService.findGradeByNumber(grade_number);
        // grade 为 double 类型
        grade.setGrade(86.0);
        Grade newGrade= gradeService.updateGradeByNumber(grade);
        System.out.println(newGrade);
        return newGrade;
    }

    // 3.2 html 修改 grade 信息
    // URL:  http://localhost:8080/updateHtmlByNumber
    @RequestMapping("/updateGradeHtmlByNumber/{student_number}/{course_number}")
    public Grade updateGradeHtmlByNumber(@PathVariable String student_number, @PathVariable String course_number,  @RequestBody Grade updatedGrade) throws IOException {
        String grade_number = student_number + ":" + course_number;
//        System.out.println("==========================");
        Grade existingGrade = gradeService.findGradeByNumber(grade_number);
        if (existingGrade != null) {
//            System.out.println("==========================");

            existingGrade.setGrade(updatedGrade.getGrade());
            gradeService.updateGradeByNumber(existingGrade);  // Assuming updateGradeByNumber method exists
//            return "grade信息更新成功：\n" + existingGrade;
            System.out.println("更新成功");
            return existingGrade;
        } else {
            System.out.println("grade信息未找到，更新失败。");
            return null;
        }
    }

    // 4.1 直接插入grade信息: 需要存在该学生与该课程,否则控制台会报错无法插入
    // URL:  http://localhost:8080/insertGradeInfo
    @RequestMapping("/insertGradeInfo")
    public String insertGradeInfo() throws IOException {
        Grade newGrade = new Grade();
        newGrade.setStudent_number("S10002");
        newGrade.setCourse_number("A101");
        newGrade.setGrade(88.0);
        // 验证传入的grade数据
        if (newGrade.getStudent_number() == null || newGrade.getGrade() == null || newGrade.getCourse_number() == null) {
            return "无效的grade数据";
        }
        // 将grade插入数据库
        int result = gradeService.addGrade(newGrade);
        newGrade = findGradeByNumber(newGrade.getStudent_number(), newGrade.getCourse_number());

        if (result > 0) {
            System.out.println(newGrade);
            return newGrade.toString();
        } else {
            return "grade信息插入失败。";
        }
    }

    // 4.2 html插入grade信息
    // URL:  http://localhost:8080/insertGradeHtmlInfo
    @RequestMapping("/insertGradeHtmlInfo")
    public Grade insertGradeHtmlInfo(@RequestBody Grade newGrade) throws IOException {
//        System.out.println("==================");
//        System.out.println(newGrade);
        // 验证传入的grade数据
        if (newGrade.getStudent_number() == null || newGrade.getGrade() == null || newGrade.getCourse_number() == null) {
            System.out.println("grade数据无效");
            return null;
        }
        // 将grade插入数据库
        int result = gradeService.addGrade(newGrade);
        newGrade = findGradeByNumber(newGrade.getStudent_number(), newGrade.getCourse_number());

        if (result > 0) {
            System.out.println("grade插入成功");
            return newGrade;
        } else {
//            return "信息插入失败。";
            System.out.println("grade插入失败");
            return null;
        }
    }
}
