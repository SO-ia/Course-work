package com.example.redis_mysql_web.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor //自动生成无参构造函数
@AllArgsConstructor
public class Stu {
    private int student_id;
    private String student_number;
    private String name;
    private String gender;

    @Override
    public String toString() {
        return "Stu{" +
                "\n\tstudent_number='" + student_number + '\'' + ',' +
                "\n\t" +"name='" + name + '\'' + ',' +
                "\n\t" +"gender='" + gender + '\'' +
                "\n" +'}';
    }
}
