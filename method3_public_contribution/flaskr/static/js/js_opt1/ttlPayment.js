function dateDiff(){
        var check_out = new Date(document.getElementById("check_out").value);
        var check_in = new Date(document.getElementById("check_in").value);
        return parseInt((check_out - check_in) / (24 * 3600 * 1000));
}

function ttlPayment(){
    var homestay_rate = document.getElementById("homestay_rate").value;
    var ttl_days = dateDiff();
    return parseInt(homestay_rate*ttl_days);
}

const dt1 = new Date()

function cal(){
if(document.getElementById("check_out")){
    document.getElementById("ttl_days").value=dateDiff();
    document.getElementById("ttl_payment").value=ttlPayment();
    document.getElementById("latest_update").value = dt1;
}  
}