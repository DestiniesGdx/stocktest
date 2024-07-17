<template>
	<div class="regist-wrap">
		<div class="ms-regist">
			<div class="ms-title">注册</div>
			<el-form :model="param" :rules="rules" ref="regist" label-width="0px" class="ms-content">
				<el-form-item prop="username">
					<el-input v-model="param.username" placeholder="用户名">
						<template #prepend>
							<el-button :icon="User"></el-button>
						</template>
					</el-input>
				</el-form-item>
				<el-form-item prop="password">
					<el-input
						placeholder="密码"
						v-model="param.password"
						@keyup.enter="submitForm(regist)"
					>
						<template #prepend>
							<el-button :icon="Lock"></el-button>
						</template>
					</el-input>
				</el-form-item>
				<div class="confirm-btn">
					<el-button type="primary" @click="submitForm(regist)">确认</el-button>
				</div>
				<div class="return-btn">
					<el-button type="primary" @click="returnLogin()">返回</el-button>
				</div>
			</el-form>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useTagsStore } from '../store/tags';
import { usePermissStore } from '../store/permiss';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { Lock, User } from '@element-plus/icons-vue';
import axios from 'axios';

interface LoginInfo {
	username: string;
	password: string;
}

const router = useRouter();
const param = reactive<LoginInfo>({
	username: '',
	password: ''
});

const rules: FormRules = {
	username: [
		{
			required: true,
			message: '请输入用户名',
			trigger: 'blur'
		}
	],
	password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
};
const permiss = usePermissStore();
const regist = ref<FormInstance>();
const submitForm = (formEl: FormInstance | undefined) => {
	if (!formEl) return;
	formEl.validate((valid: boolean) => {		
		if (valid) {
			axios.post("http://127.0.0.1:8080/userregist", JSON.stringify(param), {
      				headers: {
        				"Content-Type": "application/json",
      				},	
    			})
				.then((res) => {
					if(res.data == 'success') {
						ElMessage.success('注册成功');
						router.push('/login');
					}
					else {
						ElMessage.error('用户名重复');
						return false;
					}
				})
				.catch(function (error) {
					ElMessage.error('注册失败');
					return false;
    			});
		} else {
			ElMessage.error('用户名或密码为空');
			return false;
		}
	});
};

const returnLogin = () => {
    router.push('/login');
};

const tags = useTagsStore();
tags.clearTags();
</script>

<style scoped>
.regist-wrap {
	position: relative;
	width: 100%;
	height: 100%;
	background-image: url(../assets/img/login-bg.jpg);
	background-size: 100%;
}
.ms-title {
	width: 100%;
	line-height: 50px;
	text-align: center;
	font-size: 20px;
	color: #fff;
	border-bottom: 1px solid #ddd;
}
.ms-regist {
	position: absolute;
	left: 50%;
	top: 50%;
	width: 350px;
	margin: -190px 0 0 -175px;
	border-radius: 5px;
	background: rgba(255, 255, 255, 0.3);
	overflow: hidden;
}
.ms-content {
	padding: 30px 30px;
}
.confirm-btn {
	text-align: center;
}
.confirm-btn button {
	width: 100%;
	height: 36px;
	margin-bottom: 10px;
}

.return-btn {
	text-align: center;
}
.return-btn button {
	width: 100%;
	height: 36px;
	margin-bottom: 10px;
}

</style>
