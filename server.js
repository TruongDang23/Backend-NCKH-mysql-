const express=require('express')
const mysql=require('mysql')
const cors=require('cors')


const app=express()
app.use(cors())
app.use(express.json())

const db=mysql.createConnection({
    host:"localhost",
    user:"root",
    password:"",
    database:"account",
})

app.post('/create',(req,res)=>{
    const query="insert into login (`Username`,`Email`,`Pass`) values (?)"
    const values=[
        req.body.Username,
        req.body.Email,
        req.body.Pass,
    ]
    db.query(query,[values],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        return res.json(data)
    })
})

app.post('/login',(req,res)=>{
    const query="select * from login where `Username` = ? and `Pass` = ?"
    db.query(query,[req.body.Username,req.body.Pass],(err,data)=>{
        if(err){
            return res.json("Error")
        }
        if(data.length>0){
            return res.json("Success")
        }
        else{
            return res.json("Fail")
        }
    })
})

app.listen(3000,()=>{
    console.log("Listening at port 3000")
})

