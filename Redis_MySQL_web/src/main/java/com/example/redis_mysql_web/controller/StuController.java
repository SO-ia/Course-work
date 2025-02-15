package com.example.redis_mysql_web.controller;

import com.example.redis_mysql_web.pojo.Stu;
import com.example.redis_mysql_web.service.StuService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
public class StuController {
    @Resource
    public StuService stuService;

    // 1.访问number=S001的合法用户
    // URL:  http://localhost:8080/findStuByNumber/S004
    @RequestMapping("/findStuByNumber/{number}")
    public Stu findStuByNumber(@PathVariable String number) throws IOException {
        Stu stu= stuService.findStuByNumber(number);
        System.out.println(stu);
        return stu;
    }

    // 2.访问S009的不合法用户
    // URL:  http://localhost:8080/findStuByFliter
    @RequestMapping("/findStuByFliter")
    public Stu findStuByBloomFliter() throws IOException {
        String number="009";
        Stu stu= stuService.findStuByNumber(number);
        System.out.println(stu);
        return stu;
    }

    // 3.1 修改学生信息
    // URL:  http://localhost:8080/updateStuByNumber/S004
    @RequestMapping("/updateStuByNumber/{number}")
    public String updateStuByNumber(@PathVariable String number) throws IOException {
//        stu.setStudent_number("S004");
        Stu stu= stuService.findStuByNumber(number);
        stu.setName(stu.getName()+"修改");
        stu.setGender("F");
        String info= stuService.updateStuByNumber(stu);
        System.out.println(info);
        return info;
    }

    // 3.2 html修改学生信息
    // URL:  http://localhost:8080/updateStuHtmlByNumber
    @RequestMapping("/updateStuHtmlByNumber/{number}")
    public Stu updateStuHtmlByNumber(@PathVariable String number, @RequestBody Stu updatedStu) throws IOException {
        Stu existingStu = stuService.findStuByNumber(number);
        if (existingStu != null) {
            existingStu.setName(updatedStu.getName());
            existingStu.setGender(updatedStu.getGender());
            stuService.updateStuByNumber(existingStu);  // Assuming updateStuByNumber method exists
            System.out.println("更新成功");
            return existingStu;
        } else {
            System.out.println("学生信息未找到，更新失败。");
//            return "学生信息未找到，更新失败。";
            return null;
        }
    }

    // 4.直接插入学生信息
    // URL:  http://localhost:8080/insertStuInfo
    @RequestMapping("/insertStuInfo")
    public String insertStuInfo(){
        Stu newStu=new Stu();
        newStu.setName("AAA插入新数据");
        newStu.setGender("M");
        newStu.setStudent_number("S009");
        // 验证传入的学生数据
        if (newStu == null || newStu.getStudent_number() == null || newStu.getName() == null || newStu.getGender() == null) {
            return "无效的学生数据";
        }
        // 将学生插入数据库
        int result = stuService.addStu(newStu);

        if (result > 0) {
            return newStu.toString();
        } else {
            return "学生信息插入失败。";
        }
    }

    // 5.插入学生信息
    // URL:  http://localhost:8080/insertStuHtmlInfo
    @RequestMapping("/insertStuHtmlInfo")
    public Stu insertStuHtmlInfo(@RequestBody Stu newStu){
        // 验证传入的学生数据
        if (newStu == null || newStu.getStudent_number() == null || newStu.getName() == null || newStu.getGender() == null) {
            System.out.println("学生数据无效");
            return null;
        }
        // 将学生插入数据库
        int result = stuService.addStu(newStu);

        if (result > 0) {
            System.out.println("插入成功");
            return newStu;
        } else {
//            return "学生信息插入失败。";
            System.out.println("插入失败");
            return null;
        }
    }
}
