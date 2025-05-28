import { Router } from "express";

const subscriptionRouter = Router();

subscriptionRouter.get("/", (req, res) =>
  res.send({ title: "GET all subscriptions" })
);

subscriptionRouter.get("/:id", (req, res) =>
  res.send({ title: "GET subscriptions details" })
);

subscriptionRouter.post("/", (req, res) =>
  res.send({ title: " CREATE a new subscription" })
);

subscriptionRouter.put("/:id", (req, res) =>
  res.send({ title: "UPDATE a subscription" })
);

subscriptionRouter.delete("/:id", (req, res) =>
  res.send({ title: "DELETE a subscription" })
);

subscriptionRouter.get("/user/:id", (req, res) =>
  res.send({ title: "GET all subscriptions for a user" })
);

subscriptionRouter.put("/:id/cancel", (req, res) =>
  res.send({ title: "CANCEL a subscription" })
);

subscriptionRouter.get("/upcoming-renewals", (req, res) =>
  res.send({ title: "GET upcoming subscriptions" })
);

export default subscriptionRouter;
