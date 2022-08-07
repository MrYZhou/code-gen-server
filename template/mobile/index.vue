<template>
	<view class="" style="padding: 20px;">
		<!-- h5 app -->
		<!-- <lar-list ref="mescrollItem" :apiUrl="apiUrl">
			<template v-slot:item='{data}'>
				<view class="item-wrap">
					{{data}}
				</view>
			</template>
		</lar-list> -->

		<!-- 小程序 h5 app-->
		<!-- <lar-list ref="mescrollItem" v-model="list" :apiUrl="apiUrl">
			<view v-for="(item , index) in list" :key="index">
				<view class="item-wrap">
					<view class="">
						{{item.name}} - {{item.id}}
					</view>
				</view>
			</view>
		</lar-list> -->
	</view>
</template>
<script>
	import MescrollCompMixin from "@/uni_modules/mescroll-uni/components/mescroll-uni/mixins/mescroll-comp.js";
	export default {
		mixins: [MescrollCompMixin],
		components: {},
		mounted() {},
		data() {
			return {
				list: [],
				apiUrl: 'http://localhost:8001/plan/page',
				queryKey: {
					// 'list':'data.list'
				},
				header: {},
			}
		},
		methods: {}
	}
</script>
<style>
	.item-wrap {
		/* z-index: 999; */
		width: 100%;
		height: 100px;
		/* background-color: red; */
		border: 1px solid red;
	}
</style>
