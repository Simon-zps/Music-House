import React from "react";
import JoinRoom from "./JoinRoom";
import CreateRoom from "./CreateRoom";
import Room from "./Room";
import { BrowserRouter as Router, Route, Routes, Navigate, Link } from 'react-router-dom';
import { Grid, Typography, Button, ButtonGroup } from '@material-ui/core';
import { useState, useEffect } from "react";


export default function Home() {
    
    const [code, setCode] = useState(null)
    
    async function fetchCode() {

        try{
            const response = await fetch('/api/user-in-room');
            const data = await response.json();
            setCode(data.code);
            console.log(data.code);
        }catch(e){
            console.log(e);
        }
        
    }

    useEffect(() => {
        
        fetchCode();
    }, []);

    /** 
    useEffect(() => {
        async function fetchCode() {
            const response = await fetch('/api/user-in-room');
            const data = await response.json();
            setCode(data.code);
            console.log(data.code);
        }
        fetchCode();
    }, []);*/

    function handleChangeCode(newValue) {
        setCode(newValue);
    }

    //HOC
    function renderHome() {
        return (
            <Grid container spacing={3} >
                <Grid item xs={12} align="center">
                    <Typography variant="h3" compact="h3">
                        Music House
                    </Typography>
                </Grid>

                <Grid item xs={12} align="center">
                    <ButtonGroup disableElevation variant="contained" color="primary">
                        <Button color="primary"  component={Link} to="/join-room" >Join a room</Button>
                        <Button color="secondary"  component={Link} to="/create-room" >Create a room</Button>
                    </ButtonGroup>
                </Grid>
            </Grid>
        );
    }

    // element prop instead of component prop improves performance and React will reuse existing component like Room
    return (
        <Router>
            <Routes>
            {code ? (
                <Route path="/" element={<Navigate to={`/room/${code}`}/>} />) : (
                <Route path="/" element={renderHome()} />
                )}
                <Route path="/join-room" element={<JoinRoom />} /> 
                <Route path="/create-room" element={<CreateRoom />} />
                <Route path="/room/:code" element={<Room code={code} onChange={handleChangeCode}/>} />
            </Routes>
        </Router>
    );
}
/*{code ? (
                <Route path="/" element={<Navigate to={`/room/${code}`}/>} />) : (
                <Route path="/" element={renderHome()} />
                )}*/