package com.example.redis_mysql_web.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor //自动生成无参构造函数
@AllArgsConstructor
public class Course {
    private String course_number;
    private String course_name;
    private String course_opening_semester;
    private String course_department;

    @Override
    public String toString() {
        return "Course{" +
                "\n\tcourse_number='" + course_number + '\'' + ',' +
                "\n\t" +"course_name='" + course_name + '\'' + ',' +
                "\n\t" +"course_opening_semester='" + course_opening_semester + '\'' +
                "\n\t" +"course_department='" + course_department + '\'' +
                "\n" +'}';
    }
}
