package com.stock.demo.service;
import java.util.List;

import com.stock.demo.entity.User;
 
public interface UserService {
    List<User> queryUserList();

    String userLogin(User user);

    String userRegist(User user);

    String updatePwd(String username, String oldpwd, String newpwd);
}