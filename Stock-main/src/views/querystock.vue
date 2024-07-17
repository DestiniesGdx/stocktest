<template>
	<div>
		<div class="container" v-show = "istQuery">
			<div class="handle-box">
				<el-input v-model="query.symbol" placeholder="股票代码" class="handle-input mr10"></el-input>
				<el-button type="primary" :icon="Search" @click="handleSearch">搜索</el-button>
				<el-button type="primary" :icon="Plus" @click="handleAdd()" >添加</el-button>
			</div>
			<el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
				<el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
				<el-table-column prop="symbol" label="股票编号"></el-table-column>
				<el-table-column prop="close" label="收盘价"></el-table-column>
				<el-table-column label="涨幅" align="center">
					<template #default="scope">
						<el-tag
							:type="scope.row.state === 'increase' ? 'danger' : scope.row.state === 'decrease' ? 'success' : ''"
						>
							{{ scope.row.increase }}
						</el-tag>
					</template>
				</el-table-column>
				<el-table-column label="涨跌" align="center">
					<template #default="scope">
						<el-tag
							:type="scope.row.state === 'increase' ? 'danger' : scope.row.state === 'decrease' ? 'success' : ''"
						>
							{{ scope.row.volume }}
						</el-tag>
					</template>
				</el-table-column>

				<el-table-column label="操作" width="220" align="center">
					<template #default="scope">
						<el-button text :icon="View" @click="queryStock(scope.row.symbol, scope.$index)">
							查看
						</el-button>
						<el-button text :icon="Delete" class="red" @click="handleDelete(scope.row.symbol)">
							删除
						</el-button>
					</template>
				</el-table-column>
			</el-table>
			<div class="pagination">
				<el-pagination
					background
					layout="total, prev, pager, next"
					:current-page="query.pageIndex"
					:page-size="query.pageSize"
					:total="pageTotal"
					@current-change="handlePageChange"
				></el-pagination>
			</div>
		</div>

		<!-- 编辑弹出框 -->
		<el-dialog title="添加自选股票" v-model="editVisible" width="30%">
			<el-form label-width="70px">
				<el-form-item label="股票代码">
					<el-input v-model="form.symbol"></el-input>
				</el-form-item>
			</el-form>
			<template #footer>
				<span class="dialog-footer">
					<el-button @click="editVisible = false">取 消</el-button>
					<el-button type="primary" @click="saveAdd">确 定</el-button>
				</span>
			</template>
		</el-dialog>

		<div v-show = "isQuery" width="100%" height = "100%">
			<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1">
				<title>股票详细信息</title>
			</head>
			<body>
				<main class="container">
					<div class="returnbut">
						<h1>股票信息</h1>
						<el-button type="primary" @click="returnallstock">返回</el-button>
					</div>
					<el-table :data="onetableData" border class="table" ref="multipleTable" header-cell-class-name="table-header">
						<el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
						<el-table-column prop="symbol" label="股票编号"></el-table-column>
						<el-table-column prop="close" label="收盘价"></el-table-column>
						<el-table-column label="涨幅" align="center">
							<template #default="scope">
								<el-tag
									:type="scope.row.state === 'increase' ? 'danger' : scope.row.state === 'decrease' ? 'success' : ''"
								>
									{{ scope.row.increase }}
								</el-tag>
							</template>
						</el-table-column>
						<el-table-column label="涨跌" align="center">
							<template #default="scope">
								<el-tag
									:type="scope.row.state === 'increase' ? 'danger' : scope.row.state === 'decrease' ? 'success' : ''"
								>
									{{ scope.row.volume }}
								</el-tag>
							</template>
						</el-table-column>
					</el-table>

					<div class="tablecontainer">
						<div class = 'row'>
							<object class = 'tablek' data = "/src/assets/html/kline_with_indicators.html"></object>
							<object class = 'tablek' data = "/src/assets/html/kline_with_indicators_KDJ.html"></object>
						</div>
						<div class = 'row'>
							<object class = 'tablek' data = "/src/assets/html/kline_with_indicators_MACD.html"></object>
							<object class = 'tablek' data = "/src/assets/html/kline_with_indicators_bar.html"></object>
						</div>
					</div>
				</main>
			</body>
		</div>
	</div>
</template>

<script setup lang="ts" name="basetable">
import { ref, reactive } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete, Edit, Search, Plus, Monitor, Memo, View} from '@element-plus/icons-vue';
import { fetchData } from '../api/index';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useTagsStore } from '../store/tags';

interface TableItem {
	id: string;
	symbol: string;
	close: string;
	increase: string;
	volume: string;
	state: string;	
}

const query = reactive({
	symbol: '',
	pageIndex: 1,
	pageSize: 10
});
const tableData = ref<TableItem[]>([]);
const pageTotal = ref(0);

const username = localStorage.getItem('ms_username');
const getData = (symbol: string) => {
	axios.post("http://127.0.0.1:8080/getselect", JSON.stringify({ message: username , symbol: symbol}), {
      		headers: {
        		"Content-Type": "application/json",
      		},	
    	})
		.then((res) => {
			tableData.value = res.data;
			pageTotal.value = 1;
		})
		.catch(function (error) {
			ElMessage.error('查询失败');
    	});
};
getData('');

// 查询操作
const handleSearch = () => {
	query.pageIndex = 1;
	getData(query.symbol);
};
// 分页导航
const handlePageChange = (val: number) => {
	query.pageIndex = val;
	getData('');
};

// 删除操作
const handleDelete = (symbol: string) => {
	// 二次确认删除
	ElMessageBox.confirm('确定要删除吗？', '提示', {
		type: 'warning'
	})
	.then(() => {
		axios.post("http://127.0.0.1:8080/deleteselect", JSON.stringify({ username: username, symbol: symbol }), {
      		headers: {
        		"Content-Type": "application/json",
      		},	
    	})
		.then((res) => {
			if(res.data == 'success') {
				ElMessage.success('删除成功');
				getData('');
			}
			else if(res.data == 'fail')
				ElMessage.error('删除失败');
			else 
			    ElMessage.error(res.data);
		})
		.catch(function (error) {
			ElMessage.error('删除异常');
    	});
	})
	.catch(() => {});
};

const isQuery = ref(false);
const istQuery = ref(true);
const onetableData = ref<TableItem[]>([]);
const queryStock = (symbol: string, index: number) => {
	axios.post("http://127.0.0.1:5000/querystock", JSON.stringify({ message: symbol }), {
      		headers: {
        		"Content-Type": "application/json",
      		},	
    	})
		.then((res) => {
			if(res.data['response'] == 'success') {
				onetableData.value[0] = tableData.value[index];
				isQuery.value = true;
				istQuery.value = false;
			}
			else 
				ElMessage.error('查看失败');
		})
		.catch(function (error) {
			ElMessage.error('查询失败');
    	});
};

// 表格编辑时弹窗和保存
const editVisible = ref(false);
let form = reactive({
	symbol: ''
});
let idx: number = -1;

const handleAdd = () => {
	editVisible.value = true;
};
const saveAdd = () => {
	axios.post("http://127.0.0.1:5000/addselect", JSON.stringify({ username: username, symbol: form.symbol }), {
      		headers: {
        		"Content-Type": "application/json",
      		},	
    	})
		.then((res) => {
			if(res.data['response'] == 'success')
				ElMessage.success('添加成功');
			else if(res.data['response'] == 'wrong')
				ElMessage.error('股票代码输入有误');
			else if(res.data['response'] == 'fail')
				ElMessage.error('这支股票您已经添加过了');
			else 
				ElMessage.error('添加异常');
		})
		.catch(function (error) {
			ElMessage.error('添加失败');
    	});
	getData('');
	editVisible.value = false;
};

const returnallstock = () => {
	istQuery.value = true;
	isQuery.value = false;
}

</script>

<style scoped>
.handle-box {
	margin-bottom: 20px;
}

.handle-select {
	width: 120px;
}

.handle-input {
	width: 300px;
}
.table {
	width: 100%;
	font-size: 14px;
}
.red {
	color: #F56C6C;
}
.mr10 {
	margin-right: 10px;
}
.tablek {
    width: 930px; /* 让宽度自适应 */
    height: 470px; /* 让高度自适应 */
    margin: 0 auto; /* 居中显示，可根据需要调整 */
}
.tablecontainer {
	display: flex;
    flex-direction: column; /* 设置为纵向排列 */
    justify-content: center; /* 垂直居中排列 */
    align-items: center; /* 水平居中排列 */
}
.row {
	display: flex;
	justify-content: space-around; /* 水平居中排列 */
	width: 100%; /* 设置行的宽度为100% */
}
.returnbut{
	display: flex;
	justify-content: space-between;

}
</style>
