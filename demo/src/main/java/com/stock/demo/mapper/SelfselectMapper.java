package com.stock.demo.mapper;
import org.apache.ibatis.annotations.Mapper;

import com.stock.demo.entity.Selfselect;

import java.util.List;

@Mapper
public interface SelfselectMapper {
    List<Selfselect> querySelect(String username);

    List<Selfselect> querySymbol(String username, String symbol);

    void deleteSelect(String username, String symbol);
}