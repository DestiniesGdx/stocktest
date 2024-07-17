package com.stock.demo.controller;
 
import com.stock.demo.entity.User;
import com.stock.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;



@RestController
@CrossOrigin
public class UserController
{
    @Autowired
    private UserService userService;

    @GetMapping("/query")
    public List<User> queryUserList() {
        List<User> Users = userService.queryUserList();
        return Users;
    }

    @PostMapping("/userlogin")
    public String userLogin(@RequestBody User user) {
        return userService.userLogin(user);
    }
    
    @PostMapping("/userregist")
    public String userregist(@RequestBody User user) {
        return userService.userRegist(user);
    }
    
    @PostMapping("/updatepwd")
    public String updatePwd(@RequestBody Map<String, String> data) {
        return userService.updatePwd(data.get("username"), data.get("oldpwd"), data.get("newpwd"));
    }
}