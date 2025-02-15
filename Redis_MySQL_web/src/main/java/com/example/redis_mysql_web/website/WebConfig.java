package com.example.redis_mysql_web.website;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // 不太了解后端这部分的内容，因此电脑每次重启后都需要先修改该类
        // 需要先打开网页查看当前url的端口号，然后修改localhost:所对应的端口号
        registry.addMapping("/**").allowedOrigins("http://localhost:63342");  // Replace with your frontend URL
    }
}
