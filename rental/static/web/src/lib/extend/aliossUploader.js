layui.extend({}).define(['layer', 'upload'], function(exports) {
	var $ = layui.$,
		layer = layui.layer,
		upload = layui.upload,
		allUploaded = {},
		policyFailed = null,
		uploadData = [],
		callbackFailed = null,
		dirFailed = null,
		type,
		prefixPath,
		fid,
		layerTitle,
		filesss = {},
		successCount = 0,
		uploadCount = 0,
		filesListView = null,
		multiple = false,
		multipleFileArray = [],
		multipleFileKeyArray = [],
		uplaod = layui.upload;
	//加载样式

	var Class = function(options) {
		var that = this;
		that.options = options;
		that.init();
	};

	var Base64 = {
		_keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
		encode: function(e) {
			var t = "";
			var n, r, i, s, o, u, a;
			var f = 0;
			e = Base64._utf8_encode(e);
			while (f < e.length) {
				n = e.charCodeAt(f++);
				r = e.charCodeAt(f++);
				i = e.charCodeAt(f++);
				s = n >> 2;
				o = (n & 3) << 4 | r >> 4;
				u = (r & 15) << 2 | i >> 6;
				a = i & 63;
				if (isNaN(r)) {
					u = a = 64
				} else if (isNaN(i)) {
					a = 64
				}
				t = t + this._keyStr.charAt(s) + this._keyStr.charAt(o) + this._keyStr.charAt(u) + this._keyStr.charAt(a)
			}
			return t
		},
		decode: function(e) {
			var t = "";
			var n, r, i;
			var s, o, u, a;
			var f = 0;
			e = e.replace(/[^A-Za-z0-9+/=]/g, "");
			while (f < e.length) {
				s = this._keyStr.indexOf(e.charAt(f++));
				o = this._keyStr.indexOf(e.charAt(f++));
				u = this._keyStr.indexOf(e.charAt(f++));
				a = this._keyStr.indexOf(e.charAt(f++));
				n = s << 2 | o >> 4;
				r = (o & 15) << 4 | u >> 2;
				i = (u & 3) << 6 | a;
				t = t + String.fromCharCode(n);
				if (u != 64) {
					t = t + String.fromCharCode(r)
				}
				if (a != 64) {
					t = t + String.fromCharCode(i)
				}
			}
			t = Base64._utf8_decode(t);
			return t
		},
		_utf8_encode: function(e) {
			e = e.replace(/rn/g, "n");
			var t = "";
			for (var n = 0; n < e.length; n++) {
				var r = e.charCodeAt(n);
				if (r < 128) {
					t += String.fromCharCode(r)
				} else if (r > 127 && r < 2048) {
					t += String.fromCharCode(r >> 6 | 192);
					t += String.fromCharCode(r & 63 | 128)
				} else {
					t += String.fromCharCode(r >> 12 | 224);
					t += String.fromCharCode(r >> 6 & 63 | 128);
					t += String.fromCharCode(r & 63 | 128)
				}
			}
			return t
		},
		_utf8_decode: function(e) {
			var t = "";
			var n = 0;
			var r = c1 = c2 = 0;
			while (n < e.length) {
				r = e.charCodeAt(n);
				if (r < 128) {
					t += String.fromCharCode(r);
					n++
				} else if (r > 191 && r < 224) {
					c2 = e.charCodeAt(n + 1);
					t += String.fromCharCode((r & 31) << 6 | c2 & 63);
					n += 2
				} else {
					c2 = e.charCodeAt(n + 1);
					c3 = e.charCodeAt(n + 2);
					t += String.fromCharCode((r & 15) << 12 | (c2 & 63) << 6 | c3 & 63);
					n += 3
				}
			}
			return t
		}
	}

	Class.prototype.init = function() {
		var that = this,
			options = that.options;
		if (options.layerArea) {
			layerArea = options.layerArea;
		} else {
			layerArea = 'auto';
		}
		if (options.multiple) {
			multiple = true;
		}
		if (!that.strIsNull(that.options.fileType)) {
			fileType = that.options.fileType;
		}else{
			fileType = 'file';
		}
		if (!that.strIsNull(that.options.httpStr)) {
			httpStr = that.options.httpStr;
		} else {
			httpStr = 'https';
		}
		if (!that.strIsNull(that.options.policyFiled)) {
			policyFiled = that.options.policyFiled;
		} else {
			policyFiled = 'policy';
		}
		if (!that.strIsNull(that.options.accessidFiled)) {
			accessidFiled = that.options.accessidFiled;
		} else {
			accessidFiled = 'accessid';
		}
		if (!that.strIsNull(that.options.callbackFailed)) {
			callbackFailed = that.options.callbackFailed;
		} else {
			callbackFailed = 'callback';
		}
		if (!that.strIsNull(that.options.dirFailed)) {
			dirFailed = that.options.dirFailed;
		} else {
			dirFailed = 'test1';
		}
		if (!that.strIsNull(that.options.type)) {
			type = that.options.type;
		} else {
			type = 'assest';
		}
		if (!that.strIsNull(that.options.fid)) {
			fid = that.options.fid;
		} else {
			fid = '';
		}
		if (!that.strIsNull(that.options.codeFiled)) {
			codeFiled = that.options.codeFiled;
		} else {
			codeFiled = '';
		}
		if (!that.strIsNull(that.options.codeStatus)) {
			codeStatus = that.options.codeStatus;
		} else {
			codeStatus = 0;
		}
		if (!that.strIsNull(that.options.signatureFiled)) {
			signatureFiled = that.options.signatureFiled;
		} else {
			signatureFiled = 'signature';
		}
		if (!that.strIsNull(that.options.region)) {
			region = that.options.region;
		}
		if (!that.strIsNull(that.options.prefixPath)) {
			prefixPath = that.options.prefixPath;
		} else {
			prefixPath = '';
		}
		if (!that.strIsNull(that.options.policyUrl)) {
			policyUrl = that.options.policyUrl;
		}
		if (typeof that.options.policyData != 'undefined') {
			policyData = that.options.policyData;
		} else {
			policyData = {};
		}
		if (typeof that.options.policyHeader != 'undefined') {
			policyHeader = that.options.policyHeader;
		} else {
			policyHeader = {};
		}
		if (typeof that.options.uploadRenderData != 'undefined') {
			uploadRenderData = that.options.uploadRenderData;
		} else {
			uploadRenderData = {};
		}
		if (!that.strIsNull(that.options.policyMethod)) {
			policyMethod = that.options.policyMethod;
		} else {
			policyMethod = 'GET';
		}
		if (!that.strIsNull(that.options.bucket)) {
			bucket = that.options.bucket;
		}
		allUploaded[that.options.elm] = that.options.allUploaded;
		policyFailed = that.options.policyFailed;
		if (!that.strIsNull(that.options.layerTitle)) {
			layerTitle = that.options.layerTitle;
		} else {
			layerTitle = '上传文件到阿里云OSS';
		}
		if (multiple) {
			$(that.options.elm).on('click', function() {
				layer.open({
					type: 1,
					area: layerArea, //宽高
					resize: false,
					title: layerTitle,
					content: '<div class="layui-col-md12">' +
						'<div class="layui-card">' +
						'<div class="layui-card-body">' +
						'<div class="layui-upload">' +
						'<button type="button" class="layui-btn layui-btn-normal" id="test-upload-files">选择多文件</button>' +
						'<div class="layui-upload-list">' +
						'<table class="layui-table">' +
						'<thead>' +
						'<tr>' +
						'<th>文件名</th>' +
						'<th>大小</th>' +
						'<th>状态</th>' +
						'<th>操作</th>' +
						'</tr>' +
						'</thead>' +
						'<tbody id="test-upload-filesList"></tbody>' +
						'</table>' +
						'</div>' +
						'<button type="button" class="layui-btn" id="test-upload-filesAction">开始上传</button>' +
						'</div>' +
						'</div>' +
						'</div>' +
						'</div>',
					success: function(layero, index) {
							$('#test-upload-filesAction').on('click', function() {
								if(typeof uploadListIns.config.files == 'undefined'){
									layer.msg('请先选择要上传的文件!',{shade:'rgba(0,0,0,0)'});
									return;
								}
								layer.open({type: 3, icon: 1});
								//先获取police信息
								$.ajax({
									url: policyUrl,
									type: policyMethod,
									data: policyData,
									headers: policyHeader,
									success: function(res) {
										var successStatus = false;
										if (codeFiled) {
											if (res[codeFiled] == codeStatus) {
												successStatus = true;
											}
										} else {
											successStatus = true;
										}
										if (successStatus) {
											// 签名成功开始上传文件
											var files = uploadListIns.config.files;
											//清空原来返回的数组
											uploadData = [];
											var fileCount = 0;
											for (var filekey in files) {
												fileCount++;
											}
											res.data.signature = res.data[signatureFiled];
											res.data.accessid = res.data[accessidFiled];
											res.data.callback = res.data[callback];
											res.data.policy = res.data[policyFiled];
											for (var filekey in files) {
												var tr = filesListView.find('tr#upload-' + filekey),
													tds = tr.children();
												if (tds.eq(2).text() == '等待上传') {
													that.uploadFile(files, filekey, fileCount, res.data);
												} else {
													// successCount++;
													fileCount--;
													if(fileCount == 0){
														layer.closeAll('loading');
														layer.msg('没有文件需要上传');
													}
												}
											}
										} else {
											policyFailed(res);
										}

									},
									error: function(res) {
										policyFailed(res);
									}
								});

							})
							filesListView = $('#test-upload-filesList'),
								uploadListIns = upload.render($.extend({
									elem: '#test-upload-files',
									url: httpStr+'://'+bucket + '.' + region + '.aliyuncs.com',
									accept: fileType,
									multiple: true,
									auto: false,
									choose: function(obj) {
										var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
										//读取本地文件
										obj.preview(function(index, file, result) {
											var tr = $(['<tr id="upload-' + index + '">', '<td>' + file.name + '</td>', '<td>' + (file.size /
													1014).toFixed(
													1) + 'kb</td>', '<td>等待上传</td>', '<td>',
												'<button class="layui-btn layui-btn-mini test-upload-demo-reload layui-hide">重传</button>',
												'<button class="layui-btn layui-btn-mini layui-btn-danger test-upload-demo-delete">删除</button>',
												'</td>',
												'</tr>'
											].join(''));

											//删除
											tr.find('.test-upload-demo-delete').on('click', function() {
												delete files[index]; //删除对应的文件
												tr.remove();
												uploadListIns.config.elem.next()[0].value = ''; //清空 input file 值，以免删除后出现同名文件不可选
											});
											filesListView.append(tr);
										});
									}
								},uploadRenderData));
						} //可以自行添加按钮关闭,关闭请清空rowData
						,
					end: function() {
						if (options.success) {
							if (typeof options.success === 'function') {
								options.success();
							}
						}
					}
				});
			})
		} else {
			upload.render($.extend({
				elem: that.options.elm,
				url: httpStr+'://'+bucket + '.' + region + '.aliyuncs.com',
				accept: fileType,
				multiple: false,
				auto: false,
				choose: function(obj) {
					layer.open({type: 3, icon: 1});
					var files = this.files = obj.pushFile(); //将每次选择的文件追加到文件队列
					if (JSON.stringify(filesss) == '{}') {
						filesss = JSON.parse(JSON.stringify(files));

					} else {
						for (var file in files) {
							if (file in filesss) {
								delete files[file];
							}
						}
						filesss = JSON.parse(JSON.stringify(files));
					}
					//读取本地文件
					successCount = 0;
					//先获取police信息
					$.ajax({
						url: policyUrl,
						type: policyMethod,
						data: policyData,
						headers: policyHeader,
						success: function(res) {
							// console.log(res);
							var successStatus = false;
							if (codeFiled) {
								if (res[codeFiled] == codeStatus) {
									successStatus = true;
								}
							} else {
								successStatus = true;
							}
							if (successStatus) {
								// 签名成功开始上传文件
								res.data.signature = res.data[signatureFiled];
								res.data.accessid = res.data[accessidFiled];
								res.data.callback = res.data[callbackFailed];
								res.data.dir = res.data[dirFailed];
								res.data.policy = res.data[policyFiled];
								for (var filekey in files) {
									that.uploadFile(files, filekey, 1, res.data);
								}
							} else {
								policyFailed(res);
							}

						},
						error: function(res) {
							policyFailed(res);
						}
					});

				}
			},uploadRenderData));
		}
	};



	Class.prototype.strIsNull = function(str) {
		if (typeof str == "undefined" || str == null || str == "")
			return true;
		else
			return false;
	};



	Class.prototype.uploadFile = function(filess, filekey, fileCount, data) {
		var multipleState = this.options.multiple;
		var type = this.options.type;
		var fid = this.options.fid;
		// var dir = this.options.dir;
		multipleFileArray.push(filess[filekey]);
		data.file = filess[filekey];
		var filedata = new FormData();
		multipleFileKeyArray.push(type+'/'+fid+'/'+data.file.name);
		let cbk = data.callback;
		cbk = JSON.parse(cbk);
		// cbk.callbackBody.id = '2';
		// cbk.callbackBody.filedir ='test1';
		// cbk.callbackBody.name = data.file.name;
		// cbk = JSON.stringify(cbk);
		console.log(data);
		let t = {"callbackUrl":data.callback.callbackUrl,"callbackBody":"id="+fid+"&name="+data.file.name+"&filedir="+type+'/'+fid+'/'+"&type="+type,"callbackBodyType":"application/x-www-form-urlencoded"};
		// console.log(t);
		// console.log(tt);
		t = Base64.encode(JSON.stringify(t));
		filedata.append('key', multipleFileKeyArray[uploadCount]);
		filedata.append('policy', data.policy);
		filedata.append('OSSAccessKeyId', data.accessid);
		filedata.append('signature', data.signature);
		filedata.append('callback', t);
		filedata.append('success_action_status', 200);
		filedata.append('file', multipleFileArray[uploadCount]);
		uploadCount++;
		var upfiles = filesss;
		var that = this;
		$.ajax({
			url: data.host,
			processData: false,
			cache: false,
			contentType: false,
			type: 'POST',
			data: filedata,
			success: function() {
				var result = {
					name: multipleFileArray[successCount].name,
					type: multipleFileArray[successCount].type,
					ossUrl: httpStr+'://'+bucket + '.' + region + '.aliyuncs.com' + '/' + multipleFileKeyArray[successCount]
				};
				//成功无返回
				if (multipleState) {
					uploadData.push(result);
					var tr = filesListView.find('tr#upload-' + filekey),
						tds = tr.children();
					tds.eq(2).html('<span style="color: #5FB878;">上传成功</span>');
					tds.eq(3).html(''); //清空操作
				} else {
					uploadData = [result];
					delete upfiles[0];
				}
				successCount++;
				if (successCount == fileCount) {
					successCount = 0;
					fileCount = 0;
					uploadCount = 0;
					multipleFileArray = [];
					multipleFileKeyArray = [];
					layer.closeAll('loading')
					allUploaded[that.options.elm](uploadData);
				}

			},
			error: function(i) {
				console.log(i)
			}
		})
	};

	Class.prototype.removeArray = function(array, fileId) {
		for (var i = 0; i < array.length; i++) {
			if (array[i].fileId == fileId) {
				array.splice(i, 1);
			}
		}
		return array;
	};

	var aliossUploader = {
		render: function(options) {
			var inst = new Class(options);
			return inst;
		}

	};

	exports('aliossUploader', aliossUploader);
});
