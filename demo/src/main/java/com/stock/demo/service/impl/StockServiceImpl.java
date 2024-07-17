package com.stock.demo.service.impl;
 
import com.stock.demo.entity.Selfselect;
import com.stock.demo.entity.Stock;
import com.stock.demo.mapper.SelfselectMapper;
import com.stock.demo.mapper.StockMapper;
import com.stock.demo.service.StockService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
 
@Service
public class StockServiceImpl implements StockService
{
    @Autowired
    private SelfselectMapper selfselectMapper;
    @Autowired
    private StockMapper stockMapper;
    
    @Override
    public List<Map<String, String>> getSelect(String username, String symbol) {
        List<Selfselect> select = selfselectMapper.querySelect(username);
        List<Map<String, String>> res = new ArrayList<>();
        int cnt = 0;
        for(Selfselect now : select) {
            if(symbol.equals("") || symbol.equals(now.getSymbol())) {
                cnt++;
                List<Stock> stock = stockMapper.queryStock(now.getSymbol());
                float v = stock.get(stock.size() - 1).getClose();
                float u = stock.get(stock.size() - 2).getClose();

                Map<String, String> tmp = new HashMap<>();
                tmp.put("id", String.format("%d", cnt));
                tmp.put("symbol", now.getSymbol());
                tmp.put("close", String.format("%.2f", v));
                tmp.put("increase", String.format("%.2f", (v - u) / u) + "%");
                tmp.put("volume", String.format("%.2f", v - u));
                tmp.put("state", v > u ? "increase" : "decrease");
                res.add(tmp);
            }
        }
        return res;
    }

    @Override
    public String deleteSelect(String username, String symbol) {
        List<Selfselect> select = selfselectMapper.querySymbol(username, symbol);
        if(select.isEmpty()) return "fail";
        selfselectMapper.deleteSelect(username, symbol);
        return "success";
    }
}