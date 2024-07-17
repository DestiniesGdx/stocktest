package com.stock.demo.mapper;
import org.apache.ibatis.annotations.Mapper;

import com.stock.demo.entity.User;

import java.util.List;

@Mapper
public interface UserMapper {
    List<User> queryUserList();

    List<User> queryUser(String username);

    void insertUser(User user);

    void updatePwd(String username, String newpwd);
}