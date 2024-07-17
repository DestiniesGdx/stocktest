package com.stock.demo.controller;
 
import com.stock.demo.service.StockService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.List;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;



@RestController
@CrossOrigin
public class StockController
{
    @Autowired
    private StockService stockService;

    @PostMapping("/getselect")
    public List<Map<String, String>> getselect(@RequestBody Map<String, String> data) {
        return stockService.getSelect(data.get("message"), data.get("symbol"));
    }
    
    @PostMapping("/deleteselect")
    public String deleteSelect(@RequestBody Map<String, String> data) {
        return stockService.deleteSelect(data.get("username"), data.get("symbol"));
    }
    
}