package com.stock.demo.service;

import java.util.List;
import java.util.Map;

public interface StockService {
    List<Map<String, String>> getSelect(String username, String symbol);

    String deleteSelect(String username, String symbol);
}