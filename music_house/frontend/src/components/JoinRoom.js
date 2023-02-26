import React from "react";
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { TextField, Button, Typography, Grid } from "@mui/material";

export default function JoinRoom() {

    //Use state for code - setCode - also fetch data from api POST
    const [code, setCode] = useState("TEST")
    function handleCodeInput(e) {
        setCode(e.target.value);
    }

    function join() {
        fetch(`/api/join-room/${code}`,{
            method:"POST",
            headers: {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                code:code,
            })
    })
    .then(response => response.json())
    .then(data =>{
        console.log("Data", data)
        const redirectUrl = `/room/${code}`;
        window.location.href = redirectUrl;
    })
    }

    return (
        <Grid container spacing={1} align="center">
            <Grid item xs={12} align="center">
                <Typography variant="h4" component="h4">
                    Join a room
                </Typography>
            </Grid>

            <Grid item xs={12} >
                <TextField label="Code" placeholder="Enter code" value={code} variant="outlined" onChange={handleCodeInput} />
            </Grid>

            <Grid item xs={12}>
                <Button variant="contained" color="primary" onClick={join}>
                    Enter room
                </Button>
            </Grid>

            <Grid item xs={12}>
                <Button color="secondary" variant="contained" to="/" component={Link}>
                    Go back
                </Button>
            </Grid>
        </Grid>
    );
}