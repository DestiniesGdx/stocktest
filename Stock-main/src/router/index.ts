import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router';
import { usePermissStore } from '../store/permiss';
import Home from '../views/home.vue';

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        redirect: '/dashboard',
    },
    {
        path: '/',
        name: 'Home',
        component: Home,
        children: [
            {
                path: '/dashboard',
                name: 'dashboard',
                meta: {
                    title: '系统首页',
                    permiss: '1',
                },
                component: () => import(/* webpackChunkName: "dashboard" */ '../views/dashboard.vue'),
            },
            {
                path: '/querystock',
                name: 'querystock',
                meta: {
                    title: '自选股票',
                    permiss: '2',
                },
                component: () => import(/* webpackChunkName: "querystock" */ '../views/querystock.vue'),
            },
            {
                path: '/predict',
                name: 'predict',
                meta: {
                    title: 'AI预测',
                    permiss: '11',
                },
                component: () => import(/* webpackChunkName: "predict" */ '../views/predict.vue'),
            },
            {
                path: '/form',
                name: 'baseform',
                meta: {
                    title: '表单',
                    permiss: '5',
                },
                component: () => import(/* webpackChunkName: "form" */ '../views/form.vue'),
            },
            {
                path: '/aichat',
                name: 'aichat',
                meta: {
                    title: 'AI对话',
                    permiss: '3',
                },
                component: () => import(/* webpackChunkName: "aichat" */ '../views/aichat.vue'),
            },
            {
                path: '/about',
                name: 'about',
                meta: {
                    title: '关于作者',
                    permiss: '14',
                },
                component: () => import(/* webpackChunkName: "about" */ '../views/about.vue'),
            },
            {
                path: '/game',
                name: 'game',
                meta: {
                    title: '模拟小游戏',
                    permiss: '13',
                },
                component: () => import(/* webpackChunkName: "game" */ '../views/game.vue'),
            },
            {
                path: '/upload',
                name: 'upload',
                meta: {
                    title: '上传插件',
                    permiss: '6',
                },
                component: () => import(/* webpackChunkName: "upload" */ '../views/upload.vue'),
            },
            {
                path: '/user',
                name: 'user',
                meta: {
                    title: '个人中心',
                },
                component: () => import(/* webpackChunkName: "user" */ '../views/user.vue'),
            },
            {
                path: '/editor',
                name: 'editor',
                meta: {
                    title: '富文本编辑器',
                    permiss: '8',
                },
                component: () => import(/* webpackChunkName: "editor" */ '../views/editor.vue'),
            },
            {
                path: '/markdown',
                name: 'markdown',
                meta: {
                    title: 'markdown编辑器',
                    permiss: '9',
                },
                component: () => import(/* webpackChunkName: "markdown" */ '../views/markdown.vue'),
            },
        ],
    },
    {
        path: '/login',
        name: 'Login',
        meta: {
            title: '登录',
        },
        component: () => import(/* webpackChunkName: "login" */ '../views/login.vue'),
    },
    {
        path: '/regist',
        name: 'Regist',
        meta: {
            title: '注册',
        },
        component: () => import(/* webpackChunkName: "login" */ '../views/regist.vue'),
    },
    {
        path: '/403',
        name: '403',
        meta: {
            title: '没有权限',
        },
        component: () => import(/* webpackChunkName: "403" */ '../views/403.vue'),
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | 股票系统`;
    const role = localStorage.getItem('ms_username');
    const permiss = usePermissStore();
    if(!role && to.path == '/regist') next();
    else if (!role && to.path != '/login') {
        next('/login');
    } else if (to.meta.permiss && !permiss.key.includes(to.meta.permiss)) {
        // 如果没有权限，则进入403
        next('/403');
    } else {
        next();
    }
});

export default router;
