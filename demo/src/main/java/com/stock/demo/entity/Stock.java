package com.stock.demo.entity;
import java.util.Date;

public class Stock {
    private int id;
    private String symbol;
    private Date date;
    private float open;
    private float high;
    private float low;
    private float close;
    private int volume;

    public int getId() {
        return id;
    }    

    public void setId(int id) {
        this.id = id;
    }
    
    public String getSymbol() {
        return symbol;
    }    

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public Date getDate() {
        return date;
    }    

    public void setDate(Date date) {
        this.date = date;
    }

    public float getOpen() {
        return open;
    }    

    public void setOpen(float open) {
        this.open = open;
    }

    public float getHight() {
        return high;
    }    

    public void setHigh(float high) {
        this.high = high;
    }

    public float getLow() {
        return low;
    }    

    public void setLow(float low) {
        this.low = low;
    }

    public float getClose() {
        return close;
    }    

    public void setClose(float close) {
        this.close = close;
    }

    public int getVolume() {
        return volume;
    }    

    public void setVolume(int volume) {
        this.volume = volume;
    }
}
