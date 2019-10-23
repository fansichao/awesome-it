# HTML技术文档.md

tags: HTML JavaScript 使用技巧 2019年

## IFrame

### 在模态框中嵌入 IFrame

在模态框中嵌入 IFrame

```html
        <a href="javascript;;" class="col-3 tools-item waves-effect waves-light" data-toggle="modal" data-target="#modal-addHtml" onclick='changeHtml("银行行号识别","工作台.html")'>

        <div id="modal-addHtml" class="modal fade" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog" style="max-width: 1000px">
                <div class="modal-content" style="min-width: 600px;">
                    <div class="modal-header">
                        <h5 class="modal-title" id='modal_title'>页面</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><i class="md md-clear"></i></button>
                    </div>
                    <div class="modal-body">
                        <iframe id='modal_iframe' frameborder="0" style='width: 100%;height: calc(100vh - 100px);'></iframe>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default w-sm waves-effect" data-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-primary w-sm save-event waves-effect waves-light">确定</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function changeHtml(title,src){
                $("#modal_title").html(title);
                $("#modal_iframe").attr('src',src);
            }
        </script>

```