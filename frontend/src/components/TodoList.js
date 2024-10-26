import React, { useState, useEffect } from 'react';

function TodoList({ user }) {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const getAuthHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  });

  const fetchTodos = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/todos', {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setTodos(data);
      } else {
        console.error('Failed to fetch todos');
      }
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const addTodo = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/api/todos', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ content: newTodo }),
    });
    if (response.ok) {
      setNewTodo('');
      fetchTodos();
    }
  };

  const toggleTodo = async (id, completed) => {
    const response = await fetch(`http://localhost:5000/api/todos/${id}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ completed: !completed }),
    });
    if (response.ok) {
      fetchTodos();
    }
  };

  const deleteTodo = async (id) => {
    const response = await fetch(`http://localhost:5000/api/todos/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (response.ok) {
      fetchTodos();
    }
  };

  return (
    <div className="todo-list">
      <h2>Todo List for {user.username}</h2>
      <form onSubmit={addTodo}>
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Add new todo"
          required
        />
        <button type="submit">Add</button>
      </form>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id, todo.completed)}
            />
            <span className={todo.completed ? 'completed' : ''}>{todo.content}</span>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoList;