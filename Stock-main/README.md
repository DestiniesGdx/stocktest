## 基于https://github.com/lin-xin/vue-manage-system.git

### 基于 Vue3 + pinia + typescript + Element Plus + axios + flask + mysql + echarts + python + alpha_vantage + Phaser(HTML5)

## 安装步骤
> 因为使用vite3，node版本需要 14.18+

```
git clone https://github.com/DestiniesGdx/Stock.git      // 把模板下载到本地
cd Stock    // 进入模板目录
npm install         // 安装项目依赖，等待安装完成之后，安装失败可用 cnpm 或 yarn

// 运行
npm run dev

// 执行构建命令，生成的dist文件夹放在服务器下即可访问
npm run build
```

## 同时需要运行/src/api/py下的pyserver.py，挂梯子访问openai

## 技术栈
### Web前端：Vue(其中axios网络请求库对接Flask) + Pinia(状态管理工具，多标签页，跨组件共享状态) + typescript + Elements Plus UI组件库， echarts渲染图表+Phaser(HTML5,小游戏制作)
### 后端：Flask(python web框架连接axios), alpha_vantage(美股数据api)， mysql
