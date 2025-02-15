package com.example.redis_mysql_web.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor //自动生成无参构造函数
@AllArgsConstructor
public class Grade {
    private String course_number;
    private String course_name;
    private String student_number;
    private String student_name;
    private String grade_number;
    private Double grade;

    @Override
    public String toString() {
        return "Grade{" +
                "\n\tcourse_number='" + course_number + '\'' + ',' +
                "\n\t" + "course_name='" + course_name + '\'' + ',' +
                "\n\t" +"student_number='" + student_number + '\'' + ',' +
                "\n\t" +"student_name='" + student_name + '\'' + ',' +
//                "\n\t" +"grade_number='" + grade_number + '\'' + ',' +
                "\n\t" +"grade='" + grade + '\'' +
                "\n" +'}';
    }
}
