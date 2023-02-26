import React from "react";
import { Button, Grid, Typography, TextField, FormHelperText, FormControl, FormControlLabel, RadioGroup, Radio } from "@mui/material";
import { Link } from 'react-router-dom';
import { useState } from "react";


export default function CreateRoom() {

    const [votesToSkip, setVotesToSkip] = useState(2);
    function handleVotesChange(e) {
        setVotesToSkip(e.target.value);
    }

    const [guestPausePermission, setGuestPausePermission] = useState(true);
    function handleGuestPausePermission(e) {
        setGuestPausePermission(e.target.value === 'true');
    }

    function handleRoomButtonPressed(){
        let url = '/api/create-room'
        fetch(url, {
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                votes_to_skip:votesToSkip,
                guest_pause_permission:guestPausePermission,
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data:", data)
        })
    }

    return (
        <Grid container spacing={0} className="grid-container" >
            <Grid item xs={12} align="center">
                <Typography component='h4' variant='h4' >Create a room</Typography>
            </Grid>
            
            <Grid item xs={12} align="center">
                <FormControl component="fieldset" >
                    <FormHelperText>
                        <div align="center">Guests control of playback state</div>
                    </FormHelperText>

                    <RadioGroup row defaultValue="true" onChange={handleGuestPausePermission}>
                        <FormControlLabel value="true" control={<Radio color="primary" />} label="Play/Pause" labelPlacement="bottom" />
                        <FormControlLabel value="false" control={<Radio color="secondary" />} label="No control" labelPlacement="bottom" />
                    </RadioGroup>
                </FormControl>
            </Grid>

            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField required={true} type="number" onChange={handleVotesChange} defaultValue={2} inputProps={{min:1, style:{textAlign:"center"}}}/>
                    <FormHelperText>
                        <div align="center">
                            Votes required to skip song
                        </div>
                    </FormHelperText>
                </FormControl>
            </Grid>

            <Grid item xs={12} align="center">
                <Button color="secondary" variant="contained" onClick={handleRoomButtonPressed} >Create a room</Button>
            </Grid>

            <Grid item xs={12} align="center">
                <Button color="primary" variant="contained" component={Link} to="/">Go back</Button>
            </Grid>
            
        </Grid>
    );
}

