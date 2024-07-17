<template>
	<div>
		<div v-show = 'isQuery == false'>
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1">
				<title>AI预测</title>
			</head>
			<body>
				<main class="container">
					<div class="grid">
						<section>
							<hgroup>
								<h2>欢迎使用AI股票预测，请输入需要预测的股票</h2>
							</hgroup>
							<div class = "handle-box">
								<el-input v-model="query" placeholder="股票代码" class="handle-input mr10"></el-input>
								<el-button type="primary" :icon="Search" @click="aipredict()">预测</el-button>
							</div>
							<p id="message"></p>
						</section>
					</div>
				</main>

			</body>
		</div>
		<div v-show = "isQuery" width="100%" height = "100%">
			<body>
				<main class="container">
					<div class="returnbut">
						<h1>{{query}}预测信息</h1>
						<el-button type="primary" @click="returnallstock">返回</el-button>
					</div>
					<div v-show="isLoading" class = "gif">	
						<img src = "/src/assets/gif/loading.gif">
					</div>
					<object v-show = "isLoading == false" class = 'tablek' width="2020px" height="1010px" data = "/src/assets/html/predicted_stock_price.html"></object>
				</main>
			</body>
		</div>
	</div>
</template>

<script setup lang="ts">
import Schart from 'vue-schart';
import axios from 'axios';
import { ref, onMounted} from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete, Edit, Search, Plus, Monitor, Memo } from '@element-plus/icons-vue';

const query = ref('');
const isLoading = ref(false);
const isQuery = ref(false);
const aipredict = () => {
	isQuery.value = true;
	isLoading.value = true;
	axios.post("http://127.0.0.1:5000/aipredict", JSON.stringify({ message: query.value }), {
      		headers: {
        		"Content-Type": "application/json",
      		},	
    	})
		.then((res) => {
			if(res.data['response'] == 'success') {
				isLoading.value = false;
			}
			else if(res.data['response'] == 'fail') {
				ElMessage.error('股票代码输入有误');
			}
		})
		.catch(function (error) {
			ElMessage.error('预测失败');
    	});
};

const returnallstock = () => {
	isQuery.value = false;
}
</script>

<style scoped>
.schart-box {
	display: inline-block;
	margin: 20px;
}
.schart {
	width: 600px;
	height: 400px;
}
.content-title {
	clear: both;
	font-weight: 400;
	line-height: 50px;
	margin: 10px 0;
	font-size: 22px;
	color: #1f2f3d;
}
.returnbut{
	display: flex;
	justify-content: space-between;

}
.handle-box {
	margin-top: 20px;
}
.handle-input {
	width: 300px;
}
.mr10 {
	margin-right: 10px;
}
.gif {
	display: inline-block;
}
.gif>img {
	margin-top: 50px;
	margin-left: 20px;
	height: 100px;
	width: 100px;
}
</style>
