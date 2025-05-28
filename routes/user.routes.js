import { Router } from "express";

const userRouter = Router();

userRouter.get("/", (req, res) => res.send({ title: "GET all user" }));

userRouter.get("/:id", (req, res) =>
  res.send({ title: `GET user details with id ${req.params.id}` })
);

userRouter.post("/", (req, res) => res.send({ title: "create a new user" }));

userRouter.put("/:id", (req, res) =>
  res.send({ title: `update user with id ${req.params.id}` })
);

userRouter.delete("/:id", (req, res) =>
  res.send({ title: `delete user with id ${req.params.id}` })
);

export default userRouter;
