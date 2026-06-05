import React, { useState, useEffect } from "react";
import axios from "axios";

import {
  AppBar,
  Toolbar,
  Typography,
  Avatar,
  Container,
  Card,
  CardContent,
  CardActionArea,
  CardMedia,
  Grid,
  Paper,
  TableContainer,
  Table,
  TableBody,
  TableHead,
  TableRow,
  TableCell,
  Button,
  CircularProgress,
  Box,
} from "@mui/material";

import { styled } from "@mui/material/styles";

import ClearIcon from "@mui/icons-material/Clear";

import { useDropzone } from "react-dropzone";

import V_N_LOGO from "./V_N_LOGO.png";
import bgImage from "./bg.png";

const ColorButton = styled(Button)(() => ({
  color: "#000",
  backgroundColor: "#fff",
  borderRadius: "15px",
  padding: "15px 22px",
  fontSize: "20px",
  fontWeight: 900,

  "&:hover": {
    backgroundColor: "#ffffff7a",
  },
}));

export const ImageUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [data, setData] = useState(null);
  const [image, setImage] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  let confidence = 0;

  const sendFile = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const res = await axios.post(
        process.env.REACT_APP_API_URL,
        formData
      );

      if (res.status === 200) {
        setData(res.data);
      }
    } catch (error) {
      console.error(error);
    }

    setIsLoading(false);
  };

  const clearData = () => {
    setData(null);
    setImage(false);
    setSelectedFile(null);
    setPreview(null);
  };

  useEffect(() => {
    if (!selectedFile) {
      setPreview(null);
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreview(objectUrl);

    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  useEffect(() => {
    if (!preview) return;

    setIsLoading(true);
    sendFile();
  }, [preview]);

  const onDrop = (acceptedFiles) => {
    if (!acceptedFiles || acceptedFiles.length === 0) {
      setSelectedFile(null);
      setImage(false);
      setData(null);
      return;
    }

    setSelectedFile(acceptedFiles[0]);
    setData(null);
    setImage(true);
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "image/*": [],
    },
    multiple: false,
    onDrop,
  });

  if (data) {
    confidence = (parseFloat(data.confidence) * 100).toFixed(2);
  }

  return (
    <>
      <AppBar
        position="static"
        sx={{
          background: "#be6a77",
          boxShadow: "none",
        }}
      >
        <Toolbar>
          <Typography variant="h6">
            Potato Disease Classification
          </Typography>

          <Box sx={{ flexGrow: 1 }} />

          <Avatar src={V_N_LOGO} />
        </Toolbar>
      </AppBar>

      <Container
        maxWidth={false}
        disableGutters
        sx={{
          backgroundImage: `url(${bgImage})`,
          backgroundRepeat: "no-repeat",
          backgroundPosition: "center",
          backgroundSize: "cover",
          minHeight: "93vh",
          mt: 1,
        }}
      >
        <Grid
          container
          spacing={2}
          sx={{
            padding: "4em 1em 0 1em",
            justifyContent: "center",
            alignItems: "center"
          }}
        >
          <Grid xs={12}>
            <Card
              sx={{
                margin: "auto",
                maxWidth: 400,
                minHeight: 500,
                backgroundColor: "transparent",
                boxShadow: "0px 9px 70px 0px rgb(0 0 0 / 30%)",
                borderRadius: "15px",
              }}
            >
              {image && (
                <CardActionArea>
                  <CardMedia
                    component="img"
                    height="400"
                    image={preview}
                    alt="uploaded image"
                  />
                </CardActionArea>
              )}

              {!image && (
                <CardContent>
                  <Box
                    {...getRootProps()}
                    sx={{
                      border: "2px dashed #ccc",
                      padding: 5,
                      textAlign: "center",
                      cursor: "pointer",
                      borderRadius: "10px",
                    }}
                  >
                    <input {...getInputProps()} />

                    <Typography>
                      Drag and drop an image of a potato leaf
                    </Typography>
                  </Box>
                </CardContent>
              )}

              {data && (
                <CardContent
                  sx={{
                    backgroundColor: "white",
                    display: "flex",
                    justifyContent: "center",
                    flexDirection: "column",
                    alignItems: "center",
                  }}
                >
                  <TableContainer
                    component={Paper}
                    sx={{
                      boxShadow: "none",
                      backgroundColor: "transparent",
                    }}
                  >
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Label</TableCell>
                          <TableCell align="right">
                            Confidence
                          </TableCell>
                        </TableRow>
                      </TableHead>

                      <TableBody>
                        <TableRow>
                          <TableCell>{data.predicted_class}</TableCell>

                          <TableCell align="right">
                            {confidence}%
                          </TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              )}

              {isLoading && (
                <CardContent
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                  }}
                >
                  <CircularProgress color="secondary" />

                  <Typography variant="h6">
                    Processing...
                  </Typography>
                </CardContent>
              )}
            </Card>
          </Grid>

          {data && (
            <Grid item>
              <ColorButton
                variant="contained"
                onClick={clearData}
                startIcon={<ClearIcon />}
              >
                Clear
              </ColorButton>
            </Grid>
          )}
        </Grid>
      </Container>
    </>
  );
};
