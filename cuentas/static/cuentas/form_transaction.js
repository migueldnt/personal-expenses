Vue.component("form-transaction", {
    template: `
    <div class="box">
        <div class="field">
        <label class="label">{{typeTransaction==="add"? "Abono" : "Cargo"}} a {{accountName}}</label>
            <div class="control has-icons-left">
                <input type="number" class="input transaction-value" placeholder="Monto" >
                <span class="icon is-left">
                    <span class="material-icons">attach_money</span>
                </span>
            </div>
        </div>
        <div class="field">
            <div class="control">
                <input type="text" class="input"  placeholder="Concepto">
            </div>
        </div>
        
        <div v-if="form_expanded">
            <div class="field">
                <label class="label">Cuenta a {{typeTransaction==="add"? "cargar" : "abonar"}}</label>
                <div class="control">
                    <div class="select">
                        <select>
                            <option value="0">--Ninguna--</option>
                            <option v-for="cuenta in list_other_accounts" :key="cuenta.id" :value="cuenta.id">
                                {{cuenta.name}}
                            </option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="field">
                <label class="label">Fecha y hora</label>
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
            <button class="button is-primary" >
                <span class="icon">
                    <span class="material-icons">{{typeTransaction==="add" ? "login" : "logout"}}</span>
                </span>
                <span><strong>{{typeTransaction==="add"? "Abono" : "Cargo"}} a {{accountName.length>15 ? accountName.substring(0,15)+"..." : accountName }}</strong></span>
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
            amount:0,
            concept:"",
            date:"",
            time:"",
            affected_account_id:0,
            type_transaction: "add",

            form_expanded:false
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
        }
    },
    computed:{
        list_other_accounts:function(){
            return this.availableAccounts.filter(item=>item.id!=this.account)
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