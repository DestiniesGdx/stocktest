<template>
	<div>
		<el-row :gutter="30">
			<el-col :span="8">
				<el-card shadow="hover" class="mgb20" style="height: 280px">
					<div class="user-info">
						<el-avatar :size="120" :src="imgurl" />
						<div class="user-info-cont">
							<div class="user-info-name">{{ name }}</div>
							<div>{{ role }}</div>
						</div>
					</div>
					<div class="user-info-list">
						上次登录时间：
						<span>2023-12-08</span>
					</div>
					<div class="user-info-list">
						上次登录地点：
						<span>北京</span>
					</div>
				</el-card>
				<el-card shadow="hover" style="height: 300px">
					<template #header>
						<div class="clearfix">
							<span>语言详情</span>
						</div>
					</template>
					Vue
					<el-progress :percentage="61.6" color="#42b983"></el-progress>
					Python
					<el-progress :percentage="18.2" color="#f1e05a"></el-progress>
					TypeScript
					<el-progress :percentage="11.7"></el-progress>
					HTML
					<el-progress :percentage="3.9" color="#f56c6c"></el-progress>
					CSS
					<el-progress :percentage="3.4" color="#00FF00"></el-progress>
					JavaScript
					<el-progress :percentage="1.2" color="#cc66ff"></el-progress>
				</el-card>
			</el-col>
			<el-col :span="16">
				<el-row :gutter="20" class="mgb20">
					<el-col :span="8">
						<el-card shadow="hover" :body-style="{ padding: '0px' }">
							<div class="grid-content grid-con-1">
								<el-icon class="grid-con-icon"><User /></el-icon>
								<div class="grid-cont-right">
									<div class="grid-num">1234</div>
									<div>用户访问量</div>
								</div>
							</div>
						</el-card>
					</el-col>
					<el-col :span="8">
						<el-card shadow="hover" :body-style="{ padding: '0px' }">
							<div class="grid-content grid-con-2">
								<el-icon class="grid-con-icon"><ChatDotRound /></el-icon>
								<div class="grid-cont-right">
									<div class="grid-num">321</div>
									<div>系统消息</div>
								</div>
							</div>
						</el-card>
					</el-col>
					<el-col :span="8">
						<el-card shadow="hover" :body-style="{ padding: '0px' }">
							<div class="grid-content grid-con-3">
								<el-icon class="grid-con-icon"><Briefcase /></el-icon>
								<div class="grid-cont-right">
									<div class="grid-num">3000</div>
									<div>上证指数</div>
								</div>
							</div>
						</el-card>
					</el-col>
				</el-row>
				<el-card shadow="hover" class="mgb20" style="height: 180px">
					<h1 class = 'mgb20'>欢迎访问本网站！</h1>
					<p>本网站是关于股票训练的网站。</p>
				</el-card>
				<el-card shadow="hover" style="height: 268px">
					<template #header>
						<div class="clearfix">
							<span>时事新闻</span>
						</div>
					</template>

					<el-table :show-header="false" :data="todoList" style="width: 100%">
						<el-table-column>
							<template #default="scope">
								<div
									class="todo-item"
									:class="{
										'todo-item-del': scope.row.status
									}"
								>
									{{ scope.row.title }}
								</div>
							</template>
						</el-table-column>
					</el-table>
				</el-card>
			</el-col>
		</el-row>
	</div>
</template>

<script setup lang="ts" name="dashboard">
import Schart from 'vue-schart';
import { reactive } from 'vue';
import imgurl from '../assets/img/img.jpg';

const name = localStorage.getItem('ms_username');
const role: string = name === 'admin' ? '超级管理员' : '普通用户';

const options = {
	type: 'bar',
	title: {
		text: '最近一周各品类销售图'
	},
	xRorate: 25,
	labels: ['周一', '周二', '周三', '周四', '周五'],
	datasets: [
		{
			label: '家电',
			data: [234, 278, 270, 190, 230]
		},
		{
			label: '百货',
			data: [164, 178, 190, 135, 160]
		},
		{
			label: '食品',
			data: [144, 198, 150, 235, 120]
		}
	]
};
const options2 = {
	type: 'line',
	title: {
		text: '最近几个月各品类销售趋势图'
	},
	labels: ['6月', '7月', '8月', '9月', '10月'],
	datasets: [
		{
			label: '家电',
			data: [234, 278, 270, 190, 230]
		},
		{
			label: '百货',
			data: [164, 178, 150, 135, 160]
		},
		{
			label: '食品',
			data: [74, 118, 200, 235, 90]
		}
	]
};
const todoList = reactive([
	{
		title: '大雪节气 京西古刹卧佛寺腊梅绽放',
		status: false
	},
	{
		title: '外交部领事司：阶段性减免来华签证费',
		status: false
	},
	{
		title: '西藏自治区那曲市人大常委会原副主任李鸿伟接受纪律审查和监察调查',
		status: false
	},
	{
		title: '中老铁路通车超两年进出口货运超600万吨',
		status: false
	},
]);
</script>

<style scoped>
.el-row {
	margin-bottom: 20px;
}

.grid-content {
	display: flex;
	align-items: center;
	height: 100px;
}

.grid-cont-right {
	flex: 1;
	text-align: center;
	font-size: 14px;
	color: #999;
}

.grid-num {
	font-size: 30px;
	font-weight: bold;
}

.grid-con-icon {
	font-size: 50px;
	width: 100px;
	height: 100px;
	text-align: center;
	line-height: 100px;
	color: #fff;
}

.grid-con-1 .grid-con-icon {
	background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
	color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
	background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
	color: rgb(100, 213, 114);
}

.grid-con-3 .grid-con-icon {
	background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
	color: rgb(242, 94, 67);
}

.user-info {
	display: flex;
	align-items: center;
	padding-bottom: 20px;
	border-bottom: 2px solid #ccc;
	margin-bottom: 20px;
}

.user-info-cont {
	padding-left: 50px;
	flex: 1;
	font-size: 14px;
	color: #999;
}

.user-info-cont div:first-child {
	font-size: 30px;
	color: #222;
}

.user-info-list {
	font-size: 14px;
	color: #999;
	line-height: 25px;
}

.user-info-list span {
	margin-left: 70px;
}

.mgb20 {
	margin-bottom: 30px;
}

.todo-item {
	font-size: 14px;
}

.schart {
	width: 100%;
	height: 300px;
}
</style>
