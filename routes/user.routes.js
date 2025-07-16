import { Router } from "express";
import authorize from "../middlewares/auth.middleware.js";
import { getUsers, getUser } from "../controllers/user.controller.js";

const userRouter = Router();

userRouter.get("/", getUsers);

userRouter.get("/:id", authorize, getUser);

userRouter.post("/", (req, res) => res.send({ title: "create a new user" }));

userRouter.put("/:id", (req, res) =>
  res.send({ title: `update user with id ${req.params.id}` })
);

userRouter.delete("/:id", (req, res) =>
  res.send({ title: `delete user with id ${req.params.id}` })
);

export default userRouter;
