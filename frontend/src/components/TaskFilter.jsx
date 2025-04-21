import {
  Box, Button, Container, Grid, TextField, Typography, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Paper
} from '@mui/material';
import { useState } from 'react';
import axios from 'axios';

const TaskFilter = () => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [tasks, setTasks] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const res = await axios.post(
  'https://minicore-fastapi-react.onrender.com/api/filter-inprogress-tasks',
  {
    start_date: startDate,
    end_date: endDate,
  }
);
      setTasks(res.data);
    } catch (error) {
      alert('Error al obtener tareas');
    }
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Filtro de Tareas Atrasadas
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              label="Fecha de inicio"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              label="Fecha de fin"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={12}>
            <Button type="submit" variant="contained" fullWidth>
              Filtrar
            </Button>
          </Grid>
        </Grid>
      </Box>

      <Typography variant="h6" sx={{ mb: 2 }}>
        Total de tareas: {tasks.length}
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Empleado</TableCell>
              <TableCell>Descripción</TableCell>
              <TableCell>Fecha inicio</TableCell>
              <TableCell>Fecha fin</TableCell>
              <TableCell>Días pasados</TableCell>
              <TableCell>Proyecto</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.map((task, index) => (
              <TableRow key={index}>
                <TableCell>{task.empleado}</TableCell>
                <TableCell>{task.descripcion}</TableCell>
                <TableCell>{task.fecha_inicio}</TableCell>
                <TableCell>{task.fecha_fin}</TableCell>
                <TableCell>{task.dias_pasados}</TableCell>
                <TableCell>{task.proyecto}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default TaskFilter;
