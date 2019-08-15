/**
 * Created by wenli on 2018/7/31.
 */
var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        resources: resources,
        curFrameIndex: 1,
        curFramePath: null,
        steps: 20,
        resourceId: resourceId
    },
    methods: {
        jump: function (num) {
            num = parseInt(num);
            this.curFrameIndex += num;
            this.curFrameIndex = this.curFrameIndex < 1 ? 1 : this.curFrameIndex;
            this.curFrameIndex = this.curFrameIndex > this.resources.length ? this.resources.length : this.curFrameIndex;
            this.curFramePath = this.resources[this.curFrameIndex - 1]['path']
        }
    }
});

app.curFramePath = app.resources[app.curFrameIndex - 1]['path'];


$("#focusButton").focus();