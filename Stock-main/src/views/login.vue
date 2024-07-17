<template>
	<div class="login-wrap">
		<div class="ms-login">
			<div class="ms-title">股票系统</div>
			<el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
				<el-form-item prop="username">
					<el-input v-model="param.username" placeholder="用户名">
						<template #prepend>
							<el-button :icon="User"></el-button>
						</template>
					</el-input>
				</el-form-item>
				<el-form-item prop="password">
					<el-input
						type="password"
						placeholder="密码"
						v-model="param.password"
						@keyup.enter="submitForm(login)"
					>
						<template #prepend>
							<el-button :icon="Lock"></el-button>
						</template>
					</el-input>
				</el-form-item>
				<div class="login-btn">
					<el-button type="primary" @click="submitForm(login)">登录</el-button>
				</div>
				<div class="regist-btn">
					<el-button type="primary" @click="startRegist()">注册</el-button>
				</div>
			</el-form>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick } from 'vue';
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
const login = ref<FormInstance>();
const submitForm = (formEl: FormInstance | undefined) => {
	if (!formEl) return;
	formEl.validate((valid: boolean) => {		
		if (valid) {
			axios.post("http://127.0.0.1:8080/userlogin", JSON.stringify(param), {
      				headers: {
        				"Content-Type": "application/json",
      				},	
    			})
				.then((res) => {
					if(res.data == 'success') {
						ElMessage.success('登录成功');
						localStorage.setItem('ms_username', param.username);
						const keys = permiss.defaultList[param.username == 'admin' ? 'admin' : 'user'];
						permiss.handleSet(keys);
						localStorage.setItem('ms_keys', JSON.stringify(keys));
						router.push('/');
					}
					else {
						ElMessage.error('用户名或密码错误');
						return false;
					}
				})
				.catch(function (error) {
					ElMessage.error('登陆失败');
					return false;
    			});
		} else {
			ElMessage.error('用户名或密码为空');
			return false;
		}
	});
};

const startRegist = () => {
	router.push("/regist");
};

const tags = useTagsStore();
tags.clearTags();
</script>

<style scoped>
.login-wrap {
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
.ms-login {
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
.login-btn {
	text-align: center;
}
.login-btn button {
	width: 100%;
	height: 36px;
	margin-bottom: 10px;
}

.regist-btn {
	text-align: center;
}
.regist-btn button {
	width: 100%;
	height: 36px;
	margin-bottom: 10px;
}

</style>
