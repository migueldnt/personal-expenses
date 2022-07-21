Vue.component("form-transaction", {
    template: `
    <div class="box">
        <div class="field">
        <label class="label">{{typeTransaction==="add"? "Abono" : "Cargo"}} a {{accountName}}</label>
            <div class="control has-icons-left">
                <input type="number" class="input transaction-value" placeholder="Monto" v-model="amount" step="0.01" >
                <span class="icon is-left">
                    <span class="material-icons">attach_money</span>
                </span>
            </div>
        </div>
        <div class="field">
            <div class="control">
                <input type="text" class="input"  placeholder="Concepto" v-model="concept">
            </div>
        </div>
        
        <div v-if="form_expanded">
            <div class="field">
                <label class="label">Cuenta a {{typeTransaction==="add"? "cargar" : "abonar"}}</label>
                <div class="control">
                    <div class="select">
                        <select v-model="affected_account_id">
                            <option value="0">--Ninguna--</option>
                            <option v-for="cuenta in list_other_accounts" :key="cuenta.id" :value="cuenta.id">
                                {{cuenta.name}}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="field">
                <label class="label">Fecha: {{date_label}}</label>
                <div class="control">
                    <input type="date" class="input" v-model="date" >
                </div>
            </div>
            <div class="field">
                <div class="control">
                    <input type="time" class="input" v-model="time" >
                </div>
            </div>
        </div>
        
        <div class="mt-3">
            <button class="button" @click="expandirForm">
                <span class="icon">
                    <span class="material-icons">{{form_expanded? "expand_less" : "expand_more"}}</span>
                </span>
                <span>{{form_expanded? "Menos" : "Mas"}}</span>
            </button>
            <button class="button is-primary" @click="save" 
                :class="{'is-loading':enviando_info}" 
                :disabled="!is_valid_form || enviando_info "
            >
                <span class="icon">
                    <span class="material-icons">{{typeTransaction==="add" ? "login" : "logout"}}</span>
                </span>
                <span><strong>{{typeTransaction==="add"? "Abono" : "Cargo"}} a {{accountName?.length>15 ? accountName.substring(0,15)+"..." : accountName }}</strong></span>
            </button>
        </div>
    </div>
    `,
    props:{
        typeTransaction:{
            type:String,
            default:"add",
            required:true,
            validator:function(value){
                return ['add', 'subtract'].indexOf(value) !== -1
            }
        },
        account:{
            type:Number,
            default:0,
            required:true,
        },
        accountName:String,
        title:String,
        availableAccounts:{
            type:Array,
            required:true
        }
    },
    data:function(){
        return {
            amount:"",
            concept:"",
            date:"",
            time:"",
            affected_account_id:0,
            type_transaction: "add",

            form_expanded:false,
            enviando_info:false,
        }
    },
    mounted:function(){
        this.dateTimeToNow()
    },
    methods:{
        dateTimeToNow:function(){
            const ahora = new Date();
            this.date = formatDate(ahora)
            this.time = formatTime(ahora)
        },
        expandirForm:function(){
            this.form_expanded=!this.form_expanded
            this.dateTimeToNow()
            this.affected_account_id = 0
        },
        save:function(){
            if(!this.form_expanded){
                this.dateTimeToNow()
            }
            let formdata= {
                "type_transaction": this.typeTransaction,
                "amount":Math.abs(this.amount),
                "concept": this.concept,
                "account": this.account,
                "occurred_in": this.date+"T"+this.time,
                "affected_account_id" : this.affected_account_id,
                //"csrfmiddlewaretoken" : this.csrf
            }
            const data1=  new URLSearchParams(formdata).toString();
            console.log(data1)
            this.enviando_info=true
            let url="/rest/create-transaction/"
            fetch(url,{
                method:"POST",
                body: data1,//JSON.stringify(formdata),
                
                headers:{
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                }

            }).then(response=>response.json()).then(data=>{
                this.enviando_info = false
                if(data.status){
                    this.$emit("saved_successfully",data)
                    this.amount = "";
                    this.concept = "";
                }
            },error=>{
                alert("algo fallo, vuelve a intentarlo")
            })
        }

    },
    computed:{
        list_other_accounts:function(){
            return this.availableAccounts.filter(item=>item.id!=this.account)
        },
        is_valid_form:function(){
            const amount_valid = /^[0-9]+(\.)?[0-9]*$/.test(this.amount)
            const concept_valid = this.concept.length>2

            return amount_valid && concept_valid
        },
        date_label:function(){
            const options = {  weekday:'short',month:'long',day:'numeric',hour:'numeric',minute:'numeric'};
            return new Intl.DateTimeFormat("es-MX",options).format(new Date(this.date+"T"+this.time))
        }
    },
    watch:{
        "account":function(){
            this.affected_account_id = 0;
        }
    }
})


const formatDate=(date)=>{
    var month = pad2(date.getMonth()+1);//months (0-11)
    var day = pad2(date.getDate());//day (1-31)
    var year= date.getFullYear();
      
    return   year+"-"+month+"-"+day;

}

const formatTime = (date)=>{
    const hour = pad2(date.getHours())
    const mins = pad2(date.getMinutes())
    return `${hour}:${mins}`
}

function pad2(n) {
    return (n < 10 ? '0' : '') + n;
}

function getCookie(name) {
    var value = '; ' + document.cookie,
        parts = value.split('; ' + name + '=');
    if (parts.length == 2) return parts.pop().split(';').shift();
}