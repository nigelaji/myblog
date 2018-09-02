function init_copy_btn() {
    let codes = document.getElementsByClassName('code');

    for (let i = 0; i < codes.length; i++) {
        //为每个代码块添加复制按钮
        let copy_btn = document.createElement('div');
        copy_btn.className = 'copy-btn';
        copy_btn.dataset.content = '复制'
        codes[i].appendChild(copy_btn);

        //为每个代码块添加鼠标移入移出事件
        codes[i].onmouseover = function() {
            this.getElementsByClassName('copy-btn')[0].style.display = 'block';
        };
        codes[i].onmouseout = function() {
            this.getElementsByClassName('copy-btn')[0].style.display = 'none';
        };
    }

    //为按钮添加点击事件 复制
    new ClipboardJS('.copy-btn', {
        text: function(trigger) {
            trigger.dataset.content = '复制成功';
            trigger.style.color = 'green';
            setTimeout(function() {
                trigger.dataset.content = '复制';
                trigger.style.color = 'black';
            }, 1000);
            return trigger.parentElement.innerText;
        }
    });
}

window.onload = function() {
    init_copy_btn();
}