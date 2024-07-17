package com.stock.demo.mapper;
import org.apache.ibatis.annotations.Mapper;

import com.stock.demo.entity.Stock;

import java.util.List;

@Mapper
public interface StockMapper {
    List<Stock> queryStock(String symbol);
}