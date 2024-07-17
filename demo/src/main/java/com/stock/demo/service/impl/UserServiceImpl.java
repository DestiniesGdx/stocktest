package com.stock.demo.service.impl;
 
import com.stock.demo.entity.User;
import com.stock.demo.mapper.UserMapper;
import com.stock.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
 
import java.util.List;
 
@Service
public class UserServiceImpl implements UserService
{
    @Autowired
    private UserMapper userMapper;
    
    @Override
    public List<User> queryUserList()
    {
        return userMapper.queryUserList();
    }

    @Override
    public String userLogin(User user) {
        if(user.getUsername().equals("admin")) {
            if(user.getPassword().equals("123456"))
                return "success";
            else 
                return "fail";
        }

        List<User> person = userMapper.queryUser(user.getUsername());
        if(person.size() == 0) return "fail";
        if(person.get(0).getPassword().equals(user.getPassword()))
            return "success";
        return "fail";
    }

    @Override
    public String userRegist(User user) {
        if(user.getUsername().equals("admin")) {
            return "fail";
        }

        List<User> person = userMapper.queryUser(user.getUsername());
        if(person.size() != 0) return "fail";
        
        userMapper.insertUser(user);
        return "success";
    }

    @Override
    public String updatePwd(String username, String oldpwd, String newpwd) {
        List<User> person = userMapper.queryUser(username);
        if(!person.get(0).getPassword().equals(oldpwd))
            return "wrong";
        userMapper.updatePwd(username, newpwd);
        return "success";
    }
}