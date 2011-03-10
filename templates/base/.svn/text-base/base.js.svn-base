$.fn.flash = function(speed, func){
    $(this).hide();
    $(this).fadeIn(speed, func);
}

// http://james.padolsey.com/javascript/jquery-delay-plugin/
$.fn.delay = function(time, callback){
    // Empty function:
    jQuery.fx.step.delay = function(){};
    // Return meaningless animation, (will be added to queue)
    return this.animate({delay:1}, time, callback);
}

// 通用高亮代码,简化绑定类似于css的selector:hover效果
function cssHoverColor(selector, color){
    //如果this对象的fixColor的为真，则表示不变化效果
    $(selector).hover(function(){
        if(!$(this).data("fixColor")) {
        $(this).data("orginal-color", $(this).css("background-color"));
        $(this).css("background-color", color);
        }
    }, function(){
        if(!$(this).data("fixColor")) {
            $(this).css("background-color", $(this).data("orginal-color"));
        }
    });
};

// 通用checkbox 选择

$(function () {
    $("#checkbox-all").live("click", function(event){
        var input = $("#checkbox-table tr td input");
        if($(this).attr("checked")) {
            input.attr("checked", true);
        } else {
            input.attr("checked", false);
        }
    });

    $("#checkbox-table tbody tr td input").live("click",function(event){
        if($(this).attr("checked")){
            $(this).attr("checked", false);
        } else {
            $(this).attr("checked", true);
        }
        event.stopPropagation();
    });

    $("#checkbox-table tbody tr:not(input)").live("click", function(event){
        var td = $(event.target);
        var tr = td.parent();
        var input = tr.find("input");
        if(input.attr("checked")){
            input.attr("checked", false);
        } else {
            input.attr("checked", true);
        }
    });
});
