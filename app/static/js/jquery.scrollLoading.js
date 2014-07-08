/*!
 * jquery.scrollLoading.js
 * by zhangxinxu  http://www.zhangxinxu.com
 * 2010-11-19 v1.0
 * 2012-01-13 v1.1 偏移值计算修改 position → offset
 * 2012-09-25 v1.2 增加滚动容器参数, 回调参数
*/
(function($) {
	$.fn.scrollLoading = function(options) {
		var defaults = {
			attr: "id",
			container: $(window),
			callback: $.noop
		};
		var params = $.extend({}, defaults, options || {});
		params.cache = [];
		$(this).each(function() {
			var id = $(this).attr(params["attr"]).split('_')[1];
			//重组
			var data = {
				obj: $(this),
				id: id
			};
			params.cache.push(data);
		});
		
		var callback = function(call,id) {
			if ($.isFunction(params.callback)) {
				params.callback.call(call.get(0),id);
			}
		};
		//动态显示数据
		var loading = function() {

			var contHeight = params.container.height();
			if ($(window).get(0) === window) {
				contop = $(window).scrollTop();
			} else {
				contop = params.container.offset().top;
			}		
			
			$.each(params.cache, function(i, data) {
				var o = data.obj, id = data.id, post, posb;
				
				if (o) {
					post = o.offset().top - contop, post + o.height();
	
					if ((post >= 0 && post < contHeight) || (posb > 0 && posb <= contHeight)) {
						callback(o,id);
						data.obj = null;	
					}
				}
			});	
		};
		
		//事件触发
		//加载完毕即执行
		loading();
		//滚动执行
		params.container.bind("scroll", loading);
	};
})(jQuery);