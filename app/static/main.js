function input_check() {
    if($('#password').val&&$('#id').val){
        return true
    }else{
        return false
    }
}