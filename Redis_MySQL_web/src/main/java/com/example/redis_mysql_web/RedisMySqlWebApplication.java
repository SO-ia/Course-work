package com.example.redis_mysql_web;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "com.example.redis_mysql_web")
public class RedisMySqlWebApplication {

    public static void main(String[] args) {
        SpringApplication.run(RedisMySqlWebApplication.class, args);
    }

}
