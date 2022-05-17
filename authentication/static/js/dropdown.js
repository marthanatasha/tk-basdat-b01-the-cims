$("#nama_tokoh").change(function(){
var nama_tokoh = $(this).val();
$.ajax({
    url: "{% url 'menggunakan_apparel:get_apparel' %}",
    type: 'post',
    data: {'nama_tokoh':nama_tokoh},
    dataType: 'json',
    success:function(data){
    data = data["apparel"];
    $("#apparel").empty();
    $("#apparel").append("<option value=''>-- Pilih --</option>");
    for(var i=0; i<data.length; i++){
        $("#apparel").append("<option value='"+data[i][0]+"'>"+data[i][0]+"</option>");
    }
    }
});
});